# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-27 02:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0041_auto_20171226_2245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucs_subs_user',
            name='account_id',
            field=models.IntegerField(null=True),
        ),
    ]
