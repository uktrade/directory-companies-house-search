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
