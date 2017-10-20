import uuid

import pytest
from django.urls import reverse
from freezegun import freeze_time
from rest_framework import status

from directory_constants.constants import exred_sector_names

from . import factories


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_triage_result_retrieve_view(authed_client, authed_supplier):
    triage_result = factories.TriageResultFactory(
        sso_id=authed_supplier.sso_id
    )
    response = authed_client.get(
        reverse('export-readiness-triage-create-retrieve')
    )

    assert response.status_code == status.HTTP_200_OK
    expected_response = {
        'company_name': triage_result.company_name,
        'created': '2016-11-23T11:21:10.977518Z',
        'exported_before': triage_result.exported_before,
        'regular_exporter': triage_result.regular_exporter,
        'used_online_marketplace': triage_result.used_online_marketplace,
        'id': triage_result.pk,
        'modified': '2016-11-23T11:21:10.977518Z',
        'sector': triage_result.sector,
        'sector_name': triage_result.sector_name,
        'sole_trader': triage_result.sole_trader,
        'sso_id': triage_result.sso_id,
        'company_number': None,
    }
    assert response.json() == expected_response


@pytest.mark.django_db
def test_triage_result_retrieve_view_404(authed_client):
    response = authed_client.get(
        reverse('export-readiness-triage-create-retrieve')
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_triage_result_create_view(authed_client):
    triage_result_data = {
        'company_name': 'Acme ltd',
        'exported_before': True,
        'regular_exporter': True,
        'used_online_marketplace': True,
        'sector': exred_sector_names.SECTORS_CHOICES[0][0],
        'sole_trader': False,
    }

    response = authed_client.post(
        reverse('export-readiness-triage-create-retrieve'),
        triage_result_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    expected_response = {
        'company_name': 'Acme ltd',
        'created': '2016-11-23T11:21:10.977518Z',
        'exported_before': True,
        'regular_exporter': True,
        'used_online_marketplace': True,
        'id': response.json()['id'],
        'modified': '2016-11-23T11:21:10.977518Z',
        'sector': exred_sector_names.SECTORS_CHOICES[0][0],  # HS01
        # Animals: Live
        'sector_name': exred_sector_names.SECTORS_CHOICES[0][1],
        'sole_trader': False,
        'sso_id': 999,
        'company_number': None,
    }
    assert response.json() == expected_response


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_article_read_retrieve_view(authed_client, authed_supplier):
    article = factories.ArticleReadFactory(
        sso_id=authed_supplier.sso_id
    )
    response = authed_client.get(
        reverse('export-readiness-article-read-create-retrieve')
    )

    assert response.status_code == status.HTTP_200_OK
    expected_response = {
        'created': '2016-11-23T11:21:10.977518Z',
        'id': article.pk,
        'modified': '2016-11-23T11:21:10.977518Z',
        'sso_id': authed_supplier.sso_id,
        'article_uuid': str(article.article_uuid)
    }

    assert response.json() == expected_response


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_article_read_retrieve_404(authed_client):
    response = authed_client.get(
        reverse('export-readiness-article-read-create-retrieve')
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_article_read_create_view(authed_client):
    article_uuid = str(uuid.uuid4())
    article_data = {
        'article_uuid': article_uuid
    }

    response = authed_client.post(
        reverse('export-readiness-article-read-create-retrieve'),
        article_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    expected_response = {
        'created': '2016-11-23T11:21:10.977518Z',
        'id': response.json()['id'],
        'sso_id': 999,
        'article_uuid': article_uuid,
        'modified': '2016-11-23T11:21:10.977518Z',
    }
    assert response.json() == expected_response


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_task_completed_retrieve_view(authed_client, authed_supplier):
    task = factories.TaskCompletedFactory(
        sso_id=authed_supplier.sso_id
    )
    response = authed_client.get(
        reverse('export-readiness-task-completed-create-retrieve')
    )

    assert response.status_code == status.HTTP_200_OK
    expected_response = {
        'created': '2016-11-23T11:21:10.977518Z',
        'id': task.pk,
        'modified': '2016-11-23T11:21:10.977518Z',
        'sso_id': authed_supplier.sso_id,
        'task_uuid': str(task.task_uuid)
    }

    assert response.json() == expected_response


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_task_completed_retrieve_404(authed_client):
    response = authed_client.get(
        reverse('export-readiness-task-completed-create-retrieve')
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND


@freeze_time('2016-11-23T11:21:10.977518Z')
@pytest.mark.django_db
def test_task_completed_create_view(authed_client):
    task_uuid = str(uuid.uuid4())
    task_data = {
        'task_uuid': task_uuid
    }

    response = authed_client.post(
        reverse('export-readiness-task-completed-create-retrieve'),
        task_data,
    )
    assert response.status_code == status.HTTP_201_CREATED
    expected_response = {
        'created': '2016-11-23T11:21:10.977518Z',
        'id': response.json()['id'],
        'sso_id': 999,
        'task_uuid': task_uuid,
        'modified': '2016-11-23T11:21:10.977518Z',
    }
    assert response.json() == expected_response