import csv
import io
import tempfile
import zipfile
from contextlib import contextmanager
from urllib.parse import urlparse
from xml import etree

import requests
from django.core.management import BaseCommand
from django_pglocks import advisory_lock
from elasticsearch.client.indices import IndicesClient
from elasticsearch.helpers import bulk
from elasticsearch_dsl import Index, analyzer
from elasticsearch_dsl.index import connections
from elasticsearch.exceptions import NotFoundError

from django.utils.crypto import get_random_string
from django.conf import settings

from company.doctypes import CompanyDocType


CH_CSV_FIELDNAMES = (
    'CompanyName',
    'CompanyNumber',
    'RegAddress.CareOf',
    'RegAddress.POBox',
    'RegAddress.AddressLine1',
    'RegAddress.AddressLine2',
    'RegAddress.PostTown',
    'RegAddress.County',
    'RegAddress.Country',
    'RegAddress.PostCode',
    'CompanyCategory',
    'CompanyStatus',
    'CountryOfOrigin',
    'DissolutionDate',
    'IncorporationDate',
    'Accounts.AccountRefDay',
    'Accounts.AccountRefMonth',
    'Accounts.NextDueDate',
    'Accounts.LastMadeUpDate',
    'Accounts.AccountCategory',
    'Returns.NextDueDate',
    'Returns.LastMadeUpDate',
    'Mortgages.NumMortCharges',
    'Mortgages.NumMortOutstanding',
    'Mortgages.NumMortPartSatisfied',
    'Mortgages.NumMortSatisfied',
    'SICCode.SicText_1',
    'SICCode.SicText_2',
    'SICCode.SicText_3',
    'SICCode.SicText_4',
    'LimitedPartnerships.NumGenPartners',
    'LimitedPartnerships.NumLimPartners',
    'URI',
    'PreviousName_1.CONDATE',
    'PreviousName_1.CompanyName',
    'PreviousName_2.CONDATE',
    'PreviousName_2.CompanyName',
    'PreviousName_3.CONDATE',
    'PreviousName_3.CompanyName',
    'PreviousName_4.CONDATE',
    'PreviousName_4.CompanyName',
    'PreviousName_5.CONDATE',
    'PreviousName_5.CompanyName',
    'PreviousName_6.CONDATE',
    'PreviousName_6.CompanyName',
    'PreviousName_7.CONDATE',
    'PreviousName_7.CompanyName',
    'PreviousName_8.CONDATE',
    'PreviousName_8.CompanyName',
    'PreviousName_9.CONDATE',
    'PreviousName_9.CompanyName',
    'PreviousName_10.CONDATE',
    'PreviousName_10.CompanyName',
    'ConfStmtNextDueDate',
    'ConfStmtLastMadeUpDate'
)


ALLOWED_COUNTRIES = (
    'Wales',
    'England',
    'Scotland',
    'Great Britain',
    'United Kingdom',
    'Northern Ireland'
)

ALLOWED_COUNTRIES = [country.upper() for country in ALLOWED_COUNTRIES]


def get_ch_latest_dump_file_list(url, selector='.omega a'):
    """
    Fetch a list of last published basic data dumps from CH,
    using a given selector.
    """
    response = requests.get(url)
    parser = etree.HTMLParser()
    root = etree.parse(io.BytesIO(response.content), parser).getroot()

    url_base = urlparse(url)

    result = []
    for anchor in root.cssselect(selector):
        href = anchor.attrib['href']
        # Fix broken url
        if 'AsOneFile' not in href:
            result.append('{scheme}://{hostname}/{href}'.format(
                scheme=url_base.scheme,
                hostname=url_base.hostname,
                href=href
            ))
    return result


@contextmanager
def open_zipped_csv(file_pointer):
    """
    Enclose all the complicated logic of on-the-fly unzip->csv read in a
    nice context manager.
    """
    with zipfile.ZipFile(file_pointer) as zip_file:
        # get the first file from zip, assuming it's the only one
        csv_name = zip_file.filelist[0].filename
        with zip_file.open(csv_name) as raw_csv_file_pointer:
            # We need to read that as a text IO for CSV reader to work
            csv_fp = io.TextIOWrapper(raw_csv_file_pointer)

            yield csv.DictReader(csv_fp, fieldnames=CH_CSV_FIELDNAMES)


def iter_and_filter_csv_from_url(url, tmp_file_creator):
    """Fetch & cache zipped CSV, and then iterate though contents."""
    with tmp_file_creator() as tf:
        stream_to_file_pointer(url, tf)
        tf.seek(0, 0)

        with open_zipped_csv(tf) as csv_reader:
            next(csv_reader)  # skip the csv header
            for row in csv_reader:
                yield from process_row(row)


def stream_to_file_pointer(url, file_pointer):
    """Efficiently stream given url to given file pointer."""
    response = requests.get(url, stream=True)
    chuck_size = 4096
    for chunk in response.iter_content(chunk_size=chuck_size):
        file_pointer.write(chunk)


def process_row(row):
    if row['RegAddress.Country'] in ALLOWED_COUNTRIES:

        company = {
            'company_number': row['CompanyNumber'],
            'company_status': row['CompanyStatus']
        }
        address = {

        }
        yield company, address


class Command(BaseCommand):
    help = ""
    lock_id = None
    company_index_alias = settings.ELASTICSEARCH_COMPANY_INDEX_ALIAS
    new_company_index = None

    def __init__(self, *args, **kwargs):
        unique_id = get_random_string(length=32).lower()
        self.new_company_index = 'companies-' + unique_id
        self.new_case_study_index = 'casestudies-' + unique_id
        self.client = connections.get_connection()
        super().__init__(*args, **kwargs)

    @staticmethod
    def create_index(self, name, doc_type, alias):
        index = Index(name)
        index.doc_type(doc_type)
        index.analyzer(analyzer('english'))
        # give the index an alias (e.g, `company_alias`), so the index is used
        # when the application searches from or inserts into `campaign_alias`.
        index.aliases(**{alias: {}})  # same  as .aliases(company-alias: {})
        index.create()
        return index

    def get_indices(self, alias_name):
        indices_client = IndicesClient(client=self.client)
        try:
            return list(indices_client.get_alias(name=alias_name).keys())
        except NotFoundError:
            return []

    def create_new_indices(self):
        self.create_index(
            name=self.new_company_index,
            doc_type=CompanyDocType,
            alias=self.company_index_alias,
        )

    def get_data(self):
        endpoint = settings.CH_DOWNLOAD_URL
        ch_csv_urls = get_ch_latest_dump_file_list(endpoint)

        for csv_url in ch_csv_urls:
            ch_company_rows = iter_and_filter_csv_from_url(
                csv_url,
                tempfile.TemporaryFile
            )
            yield ch_company_rows

    def populate_new_indices(self):
        data = self.get_data()
        bulk(self.client, data)

    def delete_old_indices(self):
        for index_name in self.get_indices(self.company_index_alias):
            if index_name != self.new_company_index:
                Index(index_name).delete()

    def refresh_aliases(self):
        Index(self.company_index_alias).refresh()

    def handle(self, *args, **options):
        with advisory_lock(lock_id=self.lock_id, wait=False) as acquired:
            # if this instance was the first to call the command then
            # continue to execute the underlying management command...
            if acquired:
                self.create_new_indices()
                self.populate_new_indices()
                self.delete_old_indices()
                self.refresh_aliases()
            else:
                # ...otherwise wait for the command to finish to finish.
                with advisory_lock(lock_id=self.lock_id):
                    pass
