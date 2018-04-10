import csv
import http
import io
import urllib
import zipfile
from collections import OrderedDict
from contextlib import contextmanager
from functools import partial
from urllib.parse import urljoin

import requests
from django.conf import settings

from company.doctypes import CompanyDocType

COMPANY_STATUSES = {
    'Active': 'active',
    'Active - Proposal to Strike off': 'active',
    'Dissolved': 'dissolved',
    'Liquidation': 'liquidation',
    'RECEIVER MANAGER / ADMINISTRATIVE RECEIVER': 'liquidation',
    'Receivership': 'receivership',
    'RECEIVERSHIP': 'receivership',
    'Live but Receiver Manager on at least one charge': 'receivership',
    'In Administration': 'administration',
    'ADMINISTRATION ORDER': 'administration',
    'ADMINISTRATIVE RECEIVER': 'administration',
    'In Administration/Administrative Receiver': 'administration',
    'In Administration/Receiver Manager': 'administration',
    'Voluntary Arrangement': 'voluntary-arrangement',
    'VOLUNTARY ARRANGEMENT / ADMINISTRATIVE RECEIVER': 'voluntary-arrangement',
    'VOLUNTARY ARRANGEMENT / RECEIVER MANAGER': 'voluntary-arrangement'
}

LIMITED_COMPANY = 'ltd'
OTHER = 'other'

COMPANY_TYPES = {
    'Private Unlimited Company': 'private-unlimited',
    'Community Interest Company': LIMITED_COMPANY,
    'Private Limited Company': LIMITED_COMPANY,
    'Old Public Company': 'old-public-company',
    'PRI/LBG/NSC (Private, Limited by guarantee, '
    'no share capital, use of \'Limited\' exemption)':
        'private-limited-guarant-nsc-limited-exemption',
    'Limited Partnership': 'limited-partnership',
    'PRI/LTD BY GUAR/NSC (Private, limited by guarantee, no '
    'share capital)': 'private-limited-guarant-nsc',
    'Private Unlimited': 'private-unlimited-nsc',
    'Public Limited Company': 'plc',
    'PRIV LTD SECT. 30 (Private limited company, section 30 of '
    'the Companies Act)':
        'private-limited-shares-section-30-exemption',
    'Investment Company with Variable Capital(Umbrella)': 'icvc-umbrella',
    'Industrial and Provident Society': 'industrial-and-provident-society',
    'Northern Ireland': 'northern-ireland',
    'Limited Liability Partnership': 'llp',
    'Royal Charter Company': 'royal-charter',
    'Investment Company with Variable Capital':
        'investment-company-with-variable-capital',
    'Unregistered Company': 'unregistered-company',
    'Registered Society': 'registered-society-non-jurisdictional',
    'Other Company Type': OTHER,
    'Other company type': OTHER,
    'European Public Limited-Liability Company (SE)':
        'european-public-limited-liability-company-se',
    'Scottish Partnership': 'scottish-partnership',
    'Charitable Incorporated Organisation':
        'charitable-incorporated-organisation',
    'Scottish Charitable Incorporated Organisation':
        'scottish-charitable-incorporated-organisation',
    'Protected Cell Company': 'protected-cell-company',
    'Investment Company with Variable Capital (Securities)': 'icvc-securities',
}

MESSAGE_AUTH_FAILED = 'Auth failed with Companies House'


@contextmanager
def open_zipped_csv(file_pointer, fieldnames):
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

            yield csv.DictReader(csv_fp, fieldnames=fieldnames)


def stream_to_file_pointer(url, file_pointer):
    """Efficiently stream given url to given file pointer."""
    response = requests.get(url, stream=True)
    chuck_size = 4096
    for chunk in response.iter_content(chunk_size=chuck_size):
        file_pointer.write(chunk)


def create_company_document(row):
    address = {
        'care_of': row['RegAddress.CareOf'],
        'po_box': row['RegAddress.POBox'],
        'address_line_1': row['RegAddress.AddressLine1'],
        'address_line_2': row['RegAddress.AddressLine2'],
        'locality': row['RegAddress.PostTown'],
        'region': row['RegAddress.County'],
        'country': row['RegAddress.Country'],
        'postal_code': row['RegAddress.PostCode']
    }
    address_snippet_elements = filter(
        lambda x: x != '',
        (
            address['address_line_1'],
            address['address_line_2'],
            address['locality'],
            address['region'],
            address['country'],
            address['postal_code']
        )
    )
    address_snippet = ', '.join(address_snippet_elements)
    company = {
        'company_name': row['CompanyName'],
        'company_number': row['CompanyNumber'],
        'company_status': COMPANY_STATUSES.get(
            row['CompanyStatus'], row['CompanyStatus']
        ),
        'company_type': COMPANY_TYPES.get(
            row['CompanyCategory'], row['CompanyCategory']),
        'date_of_cessation': row['DissolutionDate'],
        'date_of_creation': row['IncorporationDate'],
        'country_of_origin': row['CountryOfOrigin'],
        'address_snippet': address_snippet,
        'address': address
    }
    return CompanyDocType(
        meta={'id': company['company_number']},
        **company
    )


class CompaniesHouseClient:
    api_key = settings.COMPANIES_HOUSE_API_KEY
    client_id = settings.COMPANIES_HOUSE_CLIENT_ID
    client_secret = settings.COMPANIES_HOUSE_CLIENT_SECRET
    make_api_url = partial(urljoin, 'https://api.companieshouse.gov.uk')
    make_oauth2_url = partial(urljoin, 'https://account.companieshouse.gov.uk')
    endpoints = {
        'profile': make_api_url('company/{number}'),
        'address': make_api_url('company/{number}/registered-office-address'),
        'search': make_api_url('search/companies'),
        'oauth2': make_oauth2_url('oauth2/authorise'),
        'oauth2-token': make_oauth2_url('oauth2/token'),
    }
    session = requests.Session()

    @classmethod
    def get_auth(cls):
        return requests.auth.HTTPBasicAuth(cls.api_key, '')

    @classmethod
    def get(cls, url, params={}):
        response = cls.session.get(url=url, params=params, auth=cls.get_auth())
        if response.status_code == http.client.UNAUTHORIZED:
            logger.error(MESSAGE_AUTH_FAILED)
        return response

    @classmethod
    def retrieve_profile(cls, number):
        url = cls.endpoints['profile'].format(number=number)
        return cls.get(url)

    @classmethod
    def retrieve_address(cls, number):
        url = cls.endpoints['address'].format(number=number)
        return cls.get(url)

    @classmethod
    def search(cls, term):
        url = cls.endpoints['search']
        return cls.get(url, params={'q': term})

    @classmethod
    def make_oauth2_url(cls, redirect_uri, company_number):
        # ordered dict to facilitate testing
        params = OrderedDict([
            ('client_id', cls.client_id),
            ('redirect_uri', redirect_uri),
            ('response_type', 'code'),
            ('scope', cls.endpoints['profile'].format(number=company_number)),
        ])
        return cls.endpoints['oauth2'] + '?' + urllib.parse.urlencode(params)

    @classmethod
    def verify_oauth2_code(cls, code, redirect_uri):
        url = cls.endpoints['oauth2-token']
        params = OrderedDict([
            ('grant_type', 'authorization_code'),
            ('code', code),
            ('client_id', cls.client_id),
            ('client_secret', cls.client_secret),
            ('redirect_uri', redirect_uri),
        ])
        return cls.session.post(url=url + '?' + urllib.parse.urlencode(params))
