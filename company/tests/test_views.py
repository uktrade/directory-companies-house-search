import pytest
from django.urls import reverse
from rest_framework import status


def test_company_search_view_missing_querystring(
        api_client, mock_signature_check
):
    url = reverse('api:search-companies')
    response = api_client.get(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {'q': ['This field is required.']}


@pytest.mark.elasticsearch_test_data
def test_company_search_view(
        api_client, mock_signature_check
):
    url = reverse('api:search-companies')
    response = api_client.get(url+'?q=yozo fass')

    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['company_name'] == '!YOZO FASS LIMITED'


@pytest.mark.elasticsearch_test_data
def test_company_registered_office_address(
        api_client, mock_signature_check
):
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
        'country': 'UNITED KINGDOM',
        'address_line_2': "236 GRAY'S INN ROAD",
        'postal_code': 'WC1X 8HB',
        'po_box': '',
        'locality': 'LONDON'
    }


@pytest.mark.elasticsearch_test_data
def test_company_registered_office_address_company_not_found(
        api_client, mock_signature_check
):
    url = reverse(
        'api:company-registered-office-address',
        kwargs={'company_number': 'foobar'}
    )
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
