# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-02 13:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0047_pm_deposit_rate'),
    ]

    operations = [
        migrations.CreateModel(
            name='pm_deposit_status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_id', models.IntegerField()),
                ('status', models.CharField(max_length=20)),
                ('inactive_time', models.DateTimeField(default='2037-01-01')),
            ],
        ),
        migrations.CreateModel(
            name='ucs_deposit_balance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_no', models.IntegerField()),
                ('club_id', models.IntegerField()),
                ('group_id', models.IntegerField()),
                ('account_id', models.IntegerField()),
                ('type_id', models.IntegerField()),
                ('deposit', models.IntegerField()),
                ('fee', models.IntegerField()),
                ('operator_id', models.IntegerField()),
                ('status_id', models.IntegerField()),
                ('active_time', models.DateTimeField(auto_now_add=True)),
                ('inactive_time', models.DateTimeField(default='2037-01-01')),
            ],
        ),
    ]
