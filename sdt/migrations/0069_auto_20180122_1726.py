# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 17:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0068_ucs_result_table_l2_is_modify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucs_result_table_l2',
            name='active_time',
            field=models.DateTimeField(default=datetime.datetime(2018, 1, 22, 17, 26, 8, 959250)),
        ),
    ]
