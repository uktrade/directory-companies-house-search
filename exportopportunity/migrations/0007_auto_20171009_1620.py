# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 16:20
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('exportopportunity', '0006_auto_20171009_1616'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExportOpportunityLegal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, null=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, null=True, verbose_name='modified')),
                ('full_name', models.CharField(max_length=1000)),
                ('job_title', models.CharField(max_length=1000)),
                ('email_address', models.EmailField(max_length=254)),
                ('company_name', models.CharField(max_length=1000)),
                ('company_website', models.URLField()),
                ('phone_number', models.CharField(max_length=30)),
                ('contact_preference', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('EMAIL', 'Email'), ('PHONE', 'Phone')], max_length=20), size=None)),
                ('campaign', models.CharField(max_length=100, null=True)),
                ('country', models.CharField(max_length=100)),
                ('advice_type', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[['', 'Other'], ('General-business-advice-and-partnership', 'General business advice and partnership'), ('Business-start-up-advice', 'Business start-up advice'), ('Drafting-of-contracts', 'Drafting of contracts'), ('Mergers-and-acquisitions', 'Mergers and acquisitions'), ('Immigration', 'Immigration'), ('Dispute-resolution', 'Dispute resolution')], max_length=30), size=None)),
                ('advice_type_other', models.CharField(blank=True, max_length=30, null=True)),
                ('target_sectors', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[['', 'Other'], ('TECHNOLOGY', 'Technology'), ('FOOD_AND_DRINK', 'Food and drink'), ('RETAIL_AND_LUXURY', 'Retail'), ('FINANCIAL_AND_PROFESSIONAL_SERVICES', 'Professional services (for example, financial services or business consulting'), ('MARINE', 'Marine'), ('ENERGY', 'Energy')], max_length=30), size=None)),
                ('target_sectors_other', models.CharField(blank=True, max_length=1000, null=True)),
                ('order_deadline', models.CharField(choices=[('1-3 MONTHS', '1 to 3 months'), ('3-6 MONTHS', '3 to 6 months'), ('6-12 MONTHS', '6 months to a year'), ('NA', 'N/A')], max_length=30)),
                ('additional_requirements', models.CharField(blank=True, max_length=1000, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='exportopportunityfood',
            options={},
        ),
    ]