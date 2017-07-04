# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-05-03 16:01
from __future__ import unicode_literals

from django.db import migrations

from company import utils


def add_company_search_index_and_populate(apps, schema_editor):
    Company = apps.get_model('company', 'Company')
    utils.rebuild_and_populate_elasticsearch_index(Company)


def remove_company_search_index(apps, schema_editor):
    companies = Index('companies')
    companies.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0040_remove_company_contact_details'),
    ]

    operations = [
        migrations.RunPython(
            add_company_search_index_and_populate, remove_company_search_index
        )
    ]
