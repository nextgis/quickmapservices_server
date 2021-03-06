# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-21 15:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qms_core', '0018_auto_20170621_1227'),
    ]

    operations = [
        migrations.AlterField(
            model_name='geoservicestatus',
            name='error_text',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
        migrations.AlterField(
            model_name='geoservicestatus',
            name='error_type',
            field=models.CharField(blank=True, choices=[('timeout', 'timeout'), ('missing layer', 'missing layer'), ('invalid response', 'invalid response'), ('wrong url', 'wrong url'), ('not found response', 'not found response'), ('unsupported service', 'unsupported service')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='geoservicestatus',
            name='http_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='geoservicestatus',
            name='http_response',
            field=models.CharField(blank=True, max_length=2048, null=True),
        ),
    ]
