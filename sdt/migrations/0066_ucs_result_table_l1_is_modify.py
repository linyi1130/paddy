# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-21 03:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0065_auto_20180120_2322'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_result_table_l1',
            name='is_modify',
            field=models.BooleanField(default=False),
        ),
    ]