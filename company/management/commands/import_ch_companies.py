import tempfile
from collections import deque
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from django.utils.timezone import now
from django_pglocks import advisory_lock
from elasticsearch.client.indices import IndicesClient
from elasticsearch.helpers import parallel_bulk
from elasticsearch_dsl import Index, analyzer
from elasticsearch_dsl.index import connections
from elasticsearch.exceptions import NotFoundError

from django.utils.crypto import get_random_string
from django.conf import settings

from company.doctypes import CompanyDocType
from company.utils import stream_to_file_pointer, open_zipped_csv, \
    create_company_document

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


class Command(BaseCommand):
    help = "Load CH companies in Elasticsearch downloading CH dumps"
    lock_id = 'es_migrations'
    company_index_alias = settings.ELASTICSEARCH_COMPANY_INDEX_ALIAS

    def __init__(self, *args, **kwargs):
        unique_id = get_random_string(length=32).lower()
        self.new_company_index = 'ch-companies-' + unique_id
        self.client = connections.get_connection()
        super().__init__(*args, **kwargs)

    def create_index(self, name, doc_type, alias):
        index = Index(name)
        index.doc_type(doc_type)
        index.analyzer(analyzer('english'))
        # give the index an alias (e.g, `company_alias`), so the index is used
        # when the application searches from or inserts into `campaign_alias`.
        index.aliases(**{alias: {}})  # same  as .aliases(company-alias: {})
        index.create()
        self.stdout.write(
            self.style.SUCCESS('New index created')
        )
        return index

    def get_indices(self, alias_name):
        indices_client = IndicesClient(client=self.client)
        try:
            return list(indices_client.get_alias(name=alias_name).keys())
        except NotFoundError:
            return []

    def create_new_index(self):
        self.create_index(
            name=self.new_company_index,
            doc_type=CompanyDocType,
            alias=self.company_index_alias,
        )

    @property
    def ch_dump_file_list(self):
        """
        Fetch a list of last published basic data dumps from CH,
        using a given selector.
        """
        url = settings.CH_DOWNLOAD_URL
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        url_base = urlparse(url)
        urls = []
        for link in soup.find(class_='omega').find_all('a'):
            href = link.get('href')
            # Fix relative url
            if 'AsOneFile' not in href:
                urls.append('{scheme}://{hostname}/{href}'.format(
                    scheme=url_base.scheme,
                    hostname=url_base.hostname,
                    href=href
                ))
        return urls

    @staticmethod
    def companies_from_csv(url, tmp_file_creator):
        """Fetch & cache zipped CSV, and then iterate though contents."""
        with tmp_file_creator() as tf:
            stream_to_file_pointer(url, tf)
            tf.seek(0, 0)

            with open_zipped_csv(
                    tf, fieldnames=CH_CSV_FIELDNAMES
            ) as csv_reader:
                next(csv_reader)  # skip the csv header
                for row in csv_reader:
                    yield create_company_document(row)

    def populate_new_index(self):
        for csv_url in self.ch_dump_file_list:
            companies = self.companies_from_csv(
                csv_url,
                tempfile.TemporaryFile
            )
            companies_dicts = (company.to_dict(True) for company in companies)
            self.stdout.write(
                self.style.SUCCESS(
                    'Downloading {url} and writing companies to ES...'.format(
                        url=csv_url))
            )
            starting_time = now()
            #  parallel_bulk is a generator that needs to be consumed
            deque(
                parallel_bulk(
                    self.client,
                    companies_dicts,
                    chunk_size=20000,
                    raise_on_exception=True
                ),
                maxlen=0
            )
            end_time = now()
            self.stdout.write(
                self.style.SUCCESS('File completed in {time}'.format(
                        time=str(end_time-starting_time)
                    ))
            )

    def delete_old_index(self):
        for index_name in self.get_indices(self.company_index_alias):
            if index_name != self.new_company_index:
                Index(index_name).delete()
        self.stdout.write(
            self.style.SUCCESS('Old index deleted')
        )

    def refresh_aliases(self):
        Index(self.company_index_alias).refresh()
        self.stdout.write(
            self.style.SUCCESS('Alias refreshed')
        )

    def handle(self, *args, **options):
        with advisory_lock(lock_id=self.lock_id, wait=False) as acquired:
            # if this instance was the first to call the command then
            # continue to execute the underlying management command...
            if acquired:
                starting_time = now()
                self.stdout.write(
                    self.style.SUCCESS('Lock acquired')
                )

                self.create_new_index()
                self.populate_new_index()
                self.delete_old_index()
                self.refresh_aliases()

                end_time = now()
                self.stdout.write(
                    self.style.SUCCESS('Import completed in {time}'.format(
                        time=str(end_time-starting_time)
                    ))
                )
