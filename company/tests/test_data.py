import pytest
from unittest import mock
from company.data import CompaniesHouseClient, CompaniesHouseException


@mock.patch('company.data.requests.get')
def test_bad_response_raises_exception(mocked_get):
    mocked_get.return_value = mock.Mock(ok=False)
    with pytest.raises(CompaniesHouseException):
        CompaniesHouseClient.get('http://foo.com')


@mock.patch('company.data.requests.get')
def test_client_good_response(mocked_get):
    mocked_get.return_value = mock.Mock(ok=True)
    assert CompaniesHouseClient.get('http://foo.com')
