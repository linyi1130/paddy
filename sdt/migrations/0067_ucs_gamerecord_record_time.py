# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 11:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0066_ucs_result_table_l1_is_modify'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_gamerecord',
            name='record_time',
            field=models.DateTimeField(null=True),
        ),
    ]