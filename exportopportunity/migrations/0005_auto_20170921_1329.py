# -*- coding: utf-8 -*-
# Generated by Django 1.9.13 on 2017-09-21 13:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exportopportunity', '0004_auto_20170919_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exportopportunity',
            name='campaign',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
