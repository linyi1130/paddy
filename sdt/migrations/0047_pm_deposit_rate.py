# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-01 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0046_auto_20180101_0250'),
    ]

    operations = [
        migrations.CreateModel(
            name='pm_deposit_rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_type', models.IntegerField()),
                ('rate', models.IntegerField()),
                ('club_id', models.IntegerField()),
                ('inactive_time', models.DateTimeField(default='2037-01-01')),
            ],
        ),
    ]
