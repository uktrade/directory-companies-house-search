from unittest import mock


import pytest
from django.urls import reverse
from healthcheck.pingdom.services import DatabaseHealthCheck


@pytest.mark.django_db
def test_pingdom_database_healthcheck_ok(client):
    response = client.get(reverse('pingdom'))
    assert response.status_code == 200


@pytest.mark.django_db
@mock.patch.object(DatabaseHealthCheck, 'check')
def test_pingdom_database_healthcheck_false(mock_database_check, client):
    mock_database_check.return_value = (
        False,
        'Database Error',
    )
    response = client.get(reverse('pingdom'))
    assert response.status_code == 500
