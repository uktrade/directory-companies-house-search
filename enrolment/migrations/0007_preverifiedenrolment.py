# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-06-26 10:43
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('enrolment', '0006_auto_20170623_1644'),
    ]

    operations = [
        migrations.CreateModel(
            name='PreVerifiedEnrolment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='modified')),
                ('company_number', models.CharField(max_length=8, validators=[django.core.validators.RegexValidator(code='invalid_company_number', message='Company number must be 8 characters', regex='^[A-Za-z0-9]{8}$')])),
                ('email_address', models.EmailField(max_length=254)),
                ('generated_for', models.CharField(help_text='The trade organisation the code was created for.', max_length=1000)),
                ('is_active', models.BooleanField(default=True)),
                ('generated_by', models.ForeignKey(help_text='The admin account that created the code.', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-modified', '-created'),
                'abstract': False,
                'get_latest_by': 'modified',
            },
        ),
    ]