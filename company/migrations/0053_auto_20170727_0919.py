# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-30 14:32
from __future__ import unicode_literals

from django.db import migrations


from company import utils


def rebuild_company_index(apps, schema_editor):
    Company = apps.get_model('company', 'Company')
    utils.rebuild_and_populate_elasticsearch_index(Company)


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0052_auto_20170719_1054'),
    ]

    operations = [
        migrations.RunPython(rebuild_company_index, migrations.RunPython.noop)
    ]
