# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-22 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0070_auto_20180122_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucs_result_table_l1',
            name='is_modify',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='ucs_result_table_l2',
            name='is_modify',
            field=models.IntegerField(default=0),
        ),
    ]