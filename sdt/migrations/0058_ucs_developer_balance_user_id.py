# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-14 05:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0057_ucs_developer_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_developer_balance',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
