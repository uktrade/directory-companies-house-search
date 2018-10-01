import re
from unittest.mock import patch

import pytest
import requests_mock

from django.conf import settings
from django.core.management import call_command
from rest_framework.test import APIClient


@pytest.fixture(autouse=True)
def mock_signature_check():
    stub = patch('conf.signature.SignatureCheckPermission.has_permission')
    stub.start()
    yield stub
    stub.stop()


@pytest.fixture
def enable_signature_check(mock_signature_check):
    mock_signature_check.stop()
    yield
    mock_signature_check.start()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def requests_mocker():
    elasticsearch_url = 'http://{address}:9200/.*'.format(
        address=settings.ELASTICSEARCH_ENDPOINT
    )
    elasticsearch_url_compiled = re.compile(elasticsearch_url)
    mocker = requests_mock.mock()
    mocker.register_uri('GET', elasticsearch_url_compiled)
    mocker.register_uri('POST', elasticsearch_url_compiled)
    mocker.register_uri('PUT', elasticsearch_url_compiled)
    mocker.register_uri('DELETE', elasticsearch_url_compiled)
    mocker.start()
    yield mocker
    mocker.stop()


@pytest.fixture(autouse=True)
def elasticsearch_test_data(request):
    if request.node.get_marker('elasticsearch_test_data'):
        # load companies before each test that uses it
        call_command('populate_es_test_data')
