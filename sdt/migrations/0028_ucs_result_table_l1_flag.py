# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-24 01:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0027_ucs_company_income'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_result_table_l1',
            name='flag',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
