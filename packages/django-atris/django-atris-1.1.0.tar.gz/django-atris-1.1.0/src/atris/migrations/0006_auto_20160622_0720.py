# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-22 11:20
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('atris', '0005_auto_20160411_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='archivedhistoricalrecord',
            name='additional_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='archivedhistoricalrecord',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
        migrations.AlterField(
            model_name='historicalrecord',
            name='additional_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='historicalrecord',
            name='data',
            field=django.contrib.postgres.fields.jsonb.JSONField(),
        ),
    ]
