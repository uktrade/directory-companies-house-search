# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2016-12-19 17:30
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0022_auto_20161212_1546'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'companies'},
        ),
        migrations.AlterModelOptions(
            name='companycasestudy',
            options={'verbose_name_plural': 'company case studies'},
        ),
        migrations.RemoveField(
            model_name='companycasestudy',
            name='year',
        ),
    ]