from unittest import mock

from requests import exceptions
import pytest
from rest_framework import status
from rest_framework.reverse import reverse

from company.data import CompaniesHouseException
from core.tests.helpers import create_response


expected_exceptions = (
    exceptions.RequestException(),
    exceptions.HTTPError(),
    exceptions.ConnectionError(),
    exceptions.ProxyError(),
    exceptions.SSLError(),
    exceptions.Timeout(),
    exceptions.ConnectTimeout(),
    exceptions.ReadTimeout(),
    CompaniesHouseException(404),
)


@pytest.fixture(autouse=True)
def mock_client_get():
    stub = mock.patch('company.data.CompaniesHouseClient.get')
    yield stub.start()
    stub.stop


def test_company_search_view_missing_querystring(api_client):
    url = reverse('api:search-companies')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'q': ['This field is required.']}


@pytest.mark.parametrize('exception', expected_exceptions)
@pytest.mark.opensearch_test_data
def test_company_search_by_name_local_fallback(
    mock_client_get, api_client, exception
):
    mock_client_get.side_effect = exception
    url = reverse('api:search-companies')
    response = api_client.get(url + '?q=yozo fass')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'items': [
            {
                'address_snippet':
                    '1 VERONICA HOUSE, WICKHAM ROAD, BROCKLEY, SE4 1NQ',
                'company_name': '!YOZO FASS LIMITED',
                'company_number': '2714021',
                'company_status': 'active',
                'company_type': 'ltd',
                'date_of_creation': '1992-05-12',
                'title': '!YOZO FASS LIMITED',
                'address': {
                    'care_of': '',
                    'po_box': '',
                    'address_line_1': '1 VERONICA HOUSE',
                    'address_line_2': 'WICKHAM ROAD',
                    'locality': 'BROCKLEY',
                    'region': '',
                    'country': 'United Kingdom',
                    'postal_code': 'SE4 1NQ'
                }
            }]
    }


@pytest.mark.opensearch_test_data
def test_company_search_by_name(mock_client_get, api_client):
    mocked_return = mock.Mock()
    mocked_return.json.return_value = {
        'items_per_page': 20,
        'page_number': 1,
        'kind': 'search#companies',
        'items': [
            {
                'description_identifier': [
                    'incorporated-on'
                ],
                'address': {
                    'postal_code': 'FOO BAR',
                    'address_line_1': '3 Whitehall place',
                    'address_line_2': 'London',
                    'country': 'United Kingdom',
                    'region': 'London',
                    'locality': 'London',
                    'premises': 'bar'
                },
                'kind': 'searchresults#company',
                'date_of_creation': '2015-04-13',
                'company_type': 'ltd',
                'snippet': '',
                'company_number': '12345678',
                'matches': {
                    'title': [
                        1,
                        5
                    ],
                    'snippet': []
                },
                'title': 'Acme',
                'company_status': 'active',
                'links': {
                    'self': '/company/12345678'
                },
                'description': 'foo',
                'address_snippet': 'foo'
            }
        ],
        'start_index': 0,
        'total_results': 1
    }
    mock_client_get.return_value = mocked_return
    url = reverse('api:search-companies')
    response = api_client.get(url + '?q=acme')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'items': [{
            'address': {
                'address_line_1': '3 Whitehall place',
                'address_line_2': 'London',
                'country': 'United Kingdom',
                'locality': 'London',
                'postal_code': 'FOO BAR',
                'premises': 'bar',
                'region': 'London'
            },
            'address_snippet': 'foo',
            'company_name': 'Acme',
            'company_number': '12345678',
            'company_status': 'active',
            'company_type': 'ltd',
            'date_of_creation': '2015-04-13',
            'title': 'Acme'
        }]
    }


@pytest.mark.opensearch_test_data
@pytest.mark.parametrize('exception', expected_exceptions)
def test_company_search_by_number_local_fallback(
    mock_client_get, api_client, exception
):
    mock_client_get.side_effect = exception
    url = reverse('api:search-companies')
    response = api_client.get(url + '?q=2714021')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'items': [
            {
                'address_snippet':
                    '1 VERONICA HOUSE, WICKHAM ROAD, BROCKLEY, SE4 1NQ',
                'company_name': '!YOZO FASS LIMITED',
                'company_number': '2714021',
                'company_status': 'active',
                'company_type': 'ltd',
                'date_of_creation': '1992-05-12',
                'title': '!YOZO FASS LIMITED',
                'address': {
                    'care_of': '',
                    'po_box': '',
                    'address_line_1': '1 VERONICA HOUSE',
                    'address_line_2': 'WICKHAM ROAD',
                    'locality': 'BROCKLEY',
                    'region': '', 'country': 'United Kingdom',
                    'postal_code': 'SE4 1NQ'
                }
            }]
    }


@pytest.mark.opensearch_test_data
def test_company_search_by_number(mock_client_get, api_client):
    mocked_return = mock.Mock()
    mocked_return.json.return_value = {
        'items_per_page': 20,
        'page_number': 1,
        'kind': 'search#companies',
        'items': [
            {
                'description_identifier': [
                    'incorporated-on'
                ],
                'address': {
                    'postal_code': 'FOO BAR',
                    'address_line_1': '3 Whitehall place',
                    'address_line_2': 'London',
                    'country': 'United Kingdom',
                    'region': 'London',
                    'locality': 'London',
                    'premises': 'bar'
                },
                'kind': 'searchresults#company',
                'date_of_creation': '2015-04-13',
                'company_type': 'ltd',
                'snippet': '',
                'company_number': '12345678',
                'matches': {
                    'title': [
                        1,
                        5
                    ],
                    'snippet': []
                },
                'title': 'Acme',
                'company_status': 'active',
                'links': {
                    'self': '/company/12345678'
                },
                'description': 'foo',
                'address_snippet': 'foo'
            }
        ],
        'start_index': 0,
        'total_results': 1
    }
    mock_client_get.return_value = mocked_return

    url = reverse('api:search-companies')
    response = api_client.get(url + '?q=12345678')

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'items': [{
            'address': {
                'address_line_1': '3 Whitehall place',
                'address_line_2': 'London',
                'country': 'United Kingdom',
                'locality': 'London',
                'postal_code': 'FOO BAR',
                'premises': 'bar',
                'region': 'London'
            },
            'address_snippet': 'foo',
            'company_name': 'Acme',
            'company_number': '12345678',
            'company_status': 'active',
            'company_type': 'ltd',
            'date_of_creation': '2015-04-13',
            'title': 'Acme'
        }]
    }


@pytest.mark.opensearch_test_data
@pytest.mark.parametrize('exception', expected_exceptions)
def test_company_registered_office_address_local_fallback(
    mock_client_get, api_client, exception
):
    mock_client_get.side_effect = exception
    url = reverse(
        'api:company-registered-office-address',
        kwargs={'company_number': '11006939'}
    )
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'address_line_1': 'C/O FRANK HIRTH 1ST FLOOR',
        'care_of': '',
        'region': '',
        'country': 'United Kingdom',
        'address_line_2': "236 GRAY'S INN ROAD",
        'postal_code': 'WC1X 8HB',
        'po_box': '',
        'locality': 'LONDON'
    }


@pytest.mark.opensearch_test_data
def test_company_registered_office_address(mock_client_get, api_client):
    mocked_return = mock.Mock()
    mocked_return.json.return_value = {
        'postal_code': 'WC1X 8HB',
        'address_line_1': 'C/O Frank Hirth 1st Floor',
        'address_line_2': '236 Grays Inn Road',
        'country': 'United Kingdom',
        'locality': 'London'
    }
    mock_client_get.return_value = mocked_return

    url = reverse(
        'api:company-registered-office-address',
        kwargs={'company_number': '11006939'}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'address_line_1': 'C/O Frank Hirth 1st Floor',
        'address_line_2': '236 Grays Inn Road',
        'country': 'United Kingdom',
        'locality': 'London',
        'postal_code': 'WC1X 8HB',
    }


@pytest.mark.opensearch_test_data
@pytest.mark.parametrize('exception', expected_exceptions)
def test_company_registered_office_address_company_not_found_local_fallback(
    mock_client_get, api_client, exception
):
    mock_client_get.side_effect = exception
    url = reverse(
        'api:company-registered-office-address',
        kwargs={'company_number': 'foobar'}
    )
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.opensearch_test_data
@pytest.mark.parametrize('exception', expected_exceptions)
def test_company_profile_company_not_found_local_fallback(
    mock_client_get, api_client, exception
):
    mock_client_get.side_effect = exception
    url = reverse(
        'api:company-profile',
        kwargs={'company_number': 'foobar'}
    )
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.opensearch_test_data
@pytest.mark.parametrize('exception', expected_exceptions)
def test_company_profile_local_fallback(
    mock_client_get, api_client, exception
):
    mock_client_get.side_effect = exception
    url = reverse(
        'api:company-profile',
        kwargs={'company_number': '11006939'}
    )
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'address_snippet': "C/O FRANK HIRTH 1ST FLOOR, 236 "
                           "GRAY'S INN ROAD, LONDON, "
                           'UNITED KINGDOM, WC1X 8HB',
        'company_name': '!NNOV8 LIMITED',
        'company_number': '11006939',
        'company_status': 'active',
        'type': 'ltd',
        'date_of_creation': '2017-10-11',
        'registered_office_address': {
            'address_line_1': 'C/O FRANK HIRTH 1ST FLOOR',
            'address_line_2': "236 GRAY'S INN ROAD",
            'care_of': '',
            'country': 'United Kingdom',
            'locality': 'LONDON',
            'po_box': '',
            'postal_code': 'WC1X 8HB',
            'region': ''
        },
        'sic_codes': ['62090'],
    }


@pytest.mark.opensearch_test_data
def test_company_profile_retrieve(mock_client_get, api_client):
    mocked_return = mock.Mock()
    mocked_return.json.return_value = {
        'company_name': '!NNOV8 LIMITED',
        'has_insolvency_history': False,
        'registered_office_is_in_dispute': False,
        'date_of_creation': '2017-10-11',
        'registered_office_address': {
            'postal_code': 'WC1X 8HB',
            'address_line_1': 'C/O Frank Hirth 1st Floor',
            'address_line_2': '236 Grays Inn Road',
            'country': 'United Kingdom',
            'locality': 'London'
        },
        'company_status': 'active',
        'type': 'ltd',
        'has_charges': False,
        'jurisdiction': 'england-wales',
        'company_number': '11006939',
        'sic_codes': [
            '62090'
        ],
        'can_file': True
    }
    mock_client_get.return_value = mocked_return

    url = reverse(
        'api:company-profile',
        kwargs={'company_number': '11006939'}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        'company_name': '!NNOV8 LIMITED',
        'company_number': '11006939',
        'company_status': 'active',
        'type': 'ltd',
        'date_of_creation': '2017-10-11',
        'registered_office_address': {
            'address_line_1': 'C/O Frank Hirth 1st Floor',
            'address_line_2': '236 Grays Inn Road',
            'country': 'United Kingdom',
            'locality': 'London',
            'postal_code': 'WC1X 8HB',
        },
        'sic_codes': ['62090'],
    }


@pytest.mark.opensearch_test_data
def test_list_officers(mock_client_get, api_client):
    expected = {
       "active_count": "integer",
       "etag": "string",
       "inactive_count": "integer",
       "items": [
          {
             "address": {
                "address_line_1": "string",
                "address_line_2": "string",
                "care_of": "string",
                "country": "string",
                "locality": "string",
                "po_box": "string",
                "postal_code": "string",
                "premises": "string",
                "region": "string"
             },
             "appointed_on": "date",
             "country_of_residence": "string",
             "date_of_birth": {
                "day": "integer",
                "month": "integer",
                "year": "integer"
             },
             "former_names": [
                {
                   "forenames": "string",
                   "surname": "string"
                }
             ],
             "identification": {
                "identification_type": "string",
                "legal_authority": "string",
                "legal_form": "string",
                "place_registered": "string",
                "registration_number": "string"
             },
             "links": {
                "officer": {
                   "appointments": "string"
                }
             },
             "name": "string",
             "nationality": "string",
             "occupation": "string",
             "officer_role": "string",
             "resigned_on": "date"
          }
       ],
       "items_per_page": "integer",
       "kind": "string",
       "links": {
          "self": "string"
       },
       "resigned_count": "integer",
       "start_index": "integer",
       "total_results": "integer"
    }
    mock_client_get.return_value = create_response(json_body=expected)

    url = reverse(
        'api:company-officers',
        kwargs={'company_number': '11006939'}
    )
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == expected


@pytest.mark.opensearch_test_data
def test_list_officers_not_found(mock_client_get, api_client):
    mock_client_get.return_value = create_response(status_code=404)

    url = reverse(
        'api:company-officers',
        kwargs={'company_number': '11006939'}
    )
    response = api_client.get(url)
    assert response.status_code == 404
