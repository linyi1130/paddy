# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-23 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0025_ucs_balance_type_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_union_balance',
            name='main_club_id',
            field=models.IntegerField(default=1000),
            preserve_default=False,
        ),
    ]