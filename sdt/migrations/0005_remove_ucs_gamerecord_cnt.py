# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 00:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0004_ucs_gamerecord_straddle'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ucs_gamerecord',
            name='cnt',
        ),
    ]
