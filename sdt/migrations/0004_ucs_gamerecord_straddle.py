# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 00:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0003_ucs_gamerecord_cnt'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_gamerecord',
            name='straddle',
            field=models.IntegerField(default=0),
        ),
    ]
