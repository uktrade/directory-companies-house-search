from functools import partial, wraps
from urllib.parse import urljoin
import logging

from elasticsearch import NotFoundError
from elasticsearch_dsl import Q
import requests
from requests.exceptions import RequestException

from django.conf import settings

from company.doctypes import CompanyDocType

logger = logging.getLogger(__name__)


class CompaniesHouseException(Exception):
    def __init__(self, status_code, *args, **kwargs):
        self.status_code = status_code
        super().__init__(*args, **kwargs)


def local_fallback(fallback_function):
    def closure(func):
        @wraps(func)
        def wrapper(class_instance, *args, **kwargs):
            try:
                return func(class_instance, *args, **kwargs)
            except (CompaniesHouseException, RequestException):
                return fallback_function(*args, **kwargs)
        return wrapper

    return closure


def retrieve_profile_from_elasticsearch(company_number):
    try:
        company = CompanyDocType.get(id=company_number)
        company = company.to_profile_dict()
        return company
    except NotFoundError:
        return None


def retrieve_address_from_elasticsearch(company_number):
    try:
        company = CompanyDocType.get(id=company_number)
        return company.address.to_dict()
    except NotFoundError:
        return None


def search_in_elasticsearch(query):
    query = Q(
        'multi_match',
        query=query,
        fields=['company_name', 'company_number']
    )
    search_object = CompanyDocType.search().query(query)
    hits = search_object.execute().to_dict()
    return [hit['_source'] for hit in hits['hits']['hits']]


class DataLoader:
    """Wrap any data source into a single class."""

    def __init__(self):
        self.companies_house_source = CompaniesHouseClient()

    @local_fallback(fallback_function=retrieve_profile_from_elasticsearch)
    def retrieve_profile(self, company_number):
        return self.companies_house_source.retrieve_profile(company_number)

    @local_fallback(fallback_function=retrieve_address_from_elasticsearch)
    def retrieve_address(self, company_number):
        return self.companies_house_source.retrieve_address(company_number)

    @local_fallback(fallback_function=search_in_elasticsearch)
    def search(self, query):
        return self.companies_house_source.search(query=query)

    def list_officers(self, company_number):
        return self.companies_house_source.list_officers(
            company_number=company_number
        )


class CompaniesHouseClient:
    api_key = settings.COMPANIES_HOUSE_API_KEY
    make_api_url = partial(urljoin, 'https://api.companieshouse.gov.uk')
    endpoints = {
        'profile': make_api_url('company/{number}'),
        'officers': make_api_url('company/{number}/officers'),
        'address': make_api_url('company/{number}/registered-office-address'),
        'search': make_api_url('search/companies'),
    }

    @classmethod
    def get_auth(cls):
        return requests.auth.HTTPBasicAuth(cls.api_key, '')

    @classmethod
    def get(cls, url, params={}):
        response = requests.get(
            url=url,
            params=params,
            auth=cls.get_auth(),
            timeout=2
        )
        if not response.ok:
            if response.status_code == 401:
                logger.error('CH auth error')
            raise CompaniesHouseException(response.status_code)
        return response

    @classmethod
    def retrieve_profile(cls, company_number):
        url = cls.endpoints['profile'].format(number=company_number)
        company = cls.get(url).json()
        return company

    @classmethod
    def retrieve_address(cls, company_number):
        url = cls.endpoints['address'].format(number=company_number)
        return cls.get(url).json()

    @classmethod
    def search(cls, query):
        url = cls.endpoints['search']
        response = cls.get(url, params={'q': query})
        results = []
        for company in response.json()['items']:
            company['company_name'] = company['title']
            results.append(company)
        return results

    @classmethod
    def list_officers(cls, company_number):
        url = cls.endpoints['officers'].format(number=company_number)
        response = cls.get(url).json()
        return response
