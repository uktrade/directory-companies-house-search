# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-03 17:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('supplier', '0002_auto_20180103_1159'),
        ('notifications', '0007_auto_20170314_1712'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplieremailnotification',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='supplier.Supplier'),
        ),
    ]