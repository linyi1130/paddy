# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-19 20:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0060_auto_20180118_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_club_user',
            name='remark',
            field=models.CharField(max_length=20, null=True),
        ),
    ]