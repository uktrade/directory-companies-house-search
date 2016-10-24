# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-10-21 12:00
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('enrolment', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='enrolment',
            name='aims',
        ),
        migrations.RemoveField(
            model_name='enrolment',
            name='company_email',
        ),
        migrations.RemoveField(
            model_name='enrolment',
            name='company_number',
        ),
        migrations.RemoveField(
            model_name='enrolment',
            name='personal_name',
        ),
        migrations.AddField(
            model_name='enrolment',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
            preserve_default=False,
        ),
    ]
