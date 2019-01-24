import datetime
from unittest import mock

import pytest
from django.conf import settings
from django.core.management import call_command

from company.doctypes import CompanyDocType

CH_HOMEPAGE_CONTENT = b"""
<div class="grid_7 push_1 omega">
<ul><li><a href="BasicCompanyDataAsOneFile-2018-02-01.zip">
BasicCompanyDataAsOneFile-2018-02-01.zip  (339Mb)</a></li></ul>
<h2>Company data as multiple files:</h2>
<ul>
<li><a href="BasicCompanyData-2018-02-01-part1_2.zip">
BasicCompanyData-2018-02-01-part1_2.zip  (69Mb)</a></li>
<li><a href="BasicCompanyData-2018-02-01-part2_2.zip">
BasicCompanyData-2018-02-01-part2_2.zip  (69Mb)</a></li>
</ul>
</div>"""


@pytest.mark.django_db
@mock.patch('company.management.commands.import_ch_companies.streaming_bulk')
@mock.patch('company.management.commands.import_ch_companies.'
            'Command.delete_old_index')
def test_import_ch_companies_streaming_bulk(
        mocked_delete_old_index,
        mocked_streaming_bulk,
        requests_mocker,
        settings
):
    settings.CH_DOWNLOAD_URL = 'http://test.com/index.html'
    requests_mocker.get(
        'http://test.com/index.html',
        content=CH_HOMEPAGE_CONTENT
    )
    with open('company/tests/ch_part1_2.zip', 'rb') as zipfile1, \
            open('company/tests/ch_part1_2.zip', 'rb') as zipfile2:
        requests_mocker.get(
            'http://test.com/BasicCompanyData-2018-02-01-part1_2.zip',
            body=zipfile1
        )
        requests_mocker.get(
            'http://test.com/BasicCompanyData-2018-02-01-part2_2.zip',
            body=zipfile2
        )
        call_command('import_ch_companies')

        data = list(mocked_streaming_bulk.call_args[0][1])
        assert mocked_streaming_bulk.called is True
        assert len(data) == 9
        data = sorted(data, key=lambda x: x['_id'])
        assert data[-1] == {
            '_id': 'SC421617',
            '_index': 'ch-companies',
            '_source': {
                'address': {
                    'address_line_1': '26 POLMUIR ROAD',
                    'address_line_2': '',
                    'care_of': '',
                    'country': 'United Kingdom',
                    'locality': 'ABERDEEN',
                    'po_box': '',
                    'postal_code': 'AB11 7SY',
                    'region': ''
                },
                'address_snippet': '26 POLMUIR ROAD, ABERDEEN, '
                                   'UNITED KINGDOM, AB11 7SY',
                'company_name': '!NSPIRED LTD',
                'company_number': 'SC421617',
                'company_status': 'active',
                'country_of_origin': 'United Kingdom',
                'date_of_creation': '2012-11-04',
                'title': '!NSPIRED LTD',
                'company_type': 'ltd',
                'sic_codes': ['70229'],
                'type': 'ltd'
            },
            '_type': 'company_doc_type'
        }
        assert mocked_delete_old_index.called is True


@pytest.mark.django_db
@mock.patch('company.management.commands.import_ch_companies.parallel_bulk')
@mock.patch('company.management.commands.import_ch_companies.'
            'Command.delete_old_index')
def test_import_ch_companies_parallel_bulk(
        mocked_delete_old_index,
        mocked_parallel_bulk,
        requests_mocker,
        settings
):
    settings.CH_DOWNLOAD_URL = 'http://test.com/index.html'
    settings.ELASTICSEARCH_USE_PARALLEL_BULK = True
    requests_mocker.get(
        'http://test.com/index.html',
        content=CH_HOMEPAGE_CONTENT
    )
    with open('company/tests/ch_part1_2.zip', 'rb') as zipfile1, \
            open('company/tests/ch_part1_2.zip', 'rb') as zipfile2:
        requests_mocker.get(
            'http://test.com/BasicCompanyData-2018-02-01-part1_2.zip',
            body=zipfile1
        )
        requests_mocker.get(
            'http://test.com/BasicCompanyData-2018-02-01-part2_2.zip',
            body=zipfile2
        )
        call_command('import_ch_companies')

        data = list(mocked_parallel_bulk.call_args[0][1])
        assert mocked_parallel_bulk.called is True
        assert len(data) == 9
        data = sorted(data, key=lambda x: x['_id'])
        assert data[-1] == {
            '_id': 'SC421617',
            '_index': 'ch-companies',
            '_source': {
                'address': {
                    'address_line_1': '26 POLMUIR ROAD',
                    'address_line_2': '',
                    'care_of': '',
                    'country': 'United Kingdom',
                    'locality': 'ABERDEEN',
                    'po_box': '',
                    'postal_code': 'AB11 7SY',
                    'region': ''
                },
                'address_snippet': '26 POLMUIR ROAD, ABERDEEN, '
                                   'UNITED KINGDOM, AB11 7SY',
                'company_name': '!NSPIRED LTD',
                'company_number': 'SC421617',
                'company_status': 'active',
                'country_of_origin': 'United Kingdom',
                'date_of_creation': '2012-11-04',
                'title': '!NSPIRED LTD',
                'company_type': 'ltd',
                'sic_codes': ['70229'],
                'type': 'ltd'
                },
            '_type': 'company_doc_type'}
        assert mocked_delete_old_index.called is True


@pytest.mark.django_db
@mock.patch('company.management.commands.import_ch_companies.IndicesClient')
@mock.patch('company.management.commands.import_ch_companies.'
            'Command.populate_new_index', mock.Mock())
def test_import_ch_companies_delete_indices(
        mocked_indices_client,
        requests_mocker
):
        mocked_indices_client().get_alias.return_value = {'foo': 'bar'}
        call_command('import_ch_companies')

        mocked_indices_client().get_alias.assert_called_once_with(
            name=settings.ELASTICSEARCH_COMPANY_INDEX_ALIAS
        )


class FalseAdvisoryMock:
    def __init__(self, *args, **kwargs):
        pass

    def __enter__(self):
        return False

    def __exit__(self, *args, **kwargs):
        pass


@pytest.mark.django_db
@mock.patch('company.management.commands.import_ch_companies.'
            'Command.create_new_index')
@mock.patch(
    'company.management.commands.import_ch_companies.advisory_lock',
    FalseAdvisoryMock
)
def test_import_ch_companies_pass_if_locked(
        mocked_create_new_index,
):
        call_command('import_ch_companies')
        assert mocked_create_new_index.called is False


def test_populate_es_test_data():
    call_command('populate_es_test_data')
    result = CompanyDocType.get(id='8209948')
    assert result.to_dict() == {
        'address': {
            'address_line_1': 'METROHOUSE 57 PEPPER ROAD',
            'address_line_2': 'HUNSLET',
            'care_of': '',
            'country': 'United Kingdom',
            'locality': 'LEEDS',
            'po_box': '',
            'postal_code': 'LS10 2RU',
            'region': 'YORKSHIRE'
        },
        'address_snippet': 'METROHOUSE 57 PEPPER ROAD, HUNSLET, LEEDS, '
                           'YORKSHIRE, LS10 2RU',
        'company_name': '! LTD',
        'company_number': '8209948',
        'company_status': 'foobar',
        'country_of_origin': 'United Kingdom',
        'date_of_creation': datetime.datetime(2012, 11, 9, 0, 0),
        'title': '! LTD',
        'company_type': 'foobar',
        'type': 'foobar',
        'sic_codes': ['99999'],
    }
