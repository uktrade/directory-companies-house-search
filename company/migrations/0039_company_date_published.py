# -*- coding: utf-8 -*-
# Generated by Django 1.9.10 on 2017-03-06 17:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0038_auto_20170306_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='date_published',
            field=models.DateField(null=True),
        ),
    ]
