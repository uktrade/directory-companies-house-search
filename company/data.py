import http
import urllib
from collections import OrderedDict
from functools import partial
from urllib.parse import urljoin

import requests
from django.conf import settings
from django.db.models import Q
from elasticsearch import NotFoundError

from company.doctypes import CompanyDocType
from company.utils import logger, MESSAGE_AUTH_FAILED


def local_fallback(fallback_function):
    def closure(func):
        def wrapper(*args, **kwargs):
            response = func(*args, **kwargs)
            if response.ok:
                return response
            else:
                return fallback_function(*args, **kwargs)
        return wrapper

    return closure


def retrieve_profile_from_es(company_number):
    try:
        company = CompanyDocType.get(id=company_number)
        company = company.to_dict()
        # in the profile Ch returns the address in a different key name
        company['registered_office_address'] = company['address']
        return company
    except NotFoundError:
        return None


def retrieve_address_from_es(company_number):
    try:
        company = CompanyDocType.get(id=company_number)
        return company.address.to_dict()
    except NotFoundError:
        return None


def search_in_es(query):
    query = Q(
        "multi_match",
        query=query,
        fields=['company_name', 'company_number']
    )
    search_object = CompanyDocType.search().query(query)
    return from_ch_results_to_dicts(search_object)


def from_ch_results_to_dicts(search_object):
    results = []
    hits = search_object.execute().to_dict()
    for hit in hits['hits']['hits']:
        company = hit['_source']
        company['title'] = company['company_name']
        results.append(company)
    return results


class DataLoader:
    """Wrap any data source into a single class."""

    def __init__(self):
        self.companies_house_source = CompaniesHouseClient()

    @local_fallback(fallback_function=retrieve_profile_from_es)
    def retrieve_profile(self, company_number):
        return self.companies_house_source.retrieve_profile(company_number)

    @local_fallback(fallback_function=retrieve_address_from_es)
    def retrieve_address(self, company_number):
        return self.companies_house_source.retrieve_address(company_number)

    @local_fallback(fallback_function=search_in_es)
    def search(self, query):
        return self.companies_house_source.search(query=query)


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
    def retrieve_profile(cls, company_number):
        url = cls.endpoints['profile'].format(number=company_number)
        return cls.get(url)

    @classmethod
    def retrieve_address(cls, company_number):
        url = cls.endpoints['address'].format(number=company_number)
        return cls.get(url)

    @classmethod
    def search(cls, query):
        url = cls.endpoints['search']
        return cls.get(url, params={'q': query})

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