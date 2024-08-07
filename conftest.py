import re
from unittest.mock import patch

import pytest
import requests_mock

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
    opensearch_url_compiled = re.compile('http://localhost:9200/.*')
    mocker = requests_mock.mock()
    mocker.register_uri('GET', opensearch_url_compiled)
    mocker.register_uri('POST', opensearch_url_compiled)
    mocker.register_uri('PUT', opensearch_url_compiled)
    mocker.register_uri('DELETE', opensearch_url_compiled)
    mocker.start()
    yield mocker
    mocker.stop()


@pytest.fixture(autouse=True)
def opensearch_test_data(request):
    if request.node.get_closest_marker('opensearch_test_data'):
        # load companies before each test that uses it
        call_command('populate_es_test_data')
