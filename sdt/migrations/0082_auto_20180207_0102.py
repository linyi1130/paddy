# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-07 01:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0081_ucs_club_user_feedback_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ucs_result_table_l2_tmp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('account_id', models.IntegerField()),
                ('user_name', models.CharField(max_length=20)),
                ('club_id', models.IntegerField(null=True)),
                ('club_name', models.CharField(max_length=20)),
                ('score', models.IntegerField()),
                ('score_final', models.IntegerField()),
                ('income_water', models.IntegerField()),
                ('waterup', models.IntegerField()),
                ('insure', models.IntegerField()),
                ('income_insure', models.IntegerField()),
                ('insure_up', models.IntegerField()),
                ('income_total', models.IntegerField()),
                ('up_total', models.IntegerField()),
                ('delivery', models.IntegerField()),
                ('feedback', models.IntegerField()),
                ('game_no', models.CharField(max_length=40)),
                ('operator_id', models.IntegerField(null=True)),
                ('active_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('inactive_time', models.DateTimeField(default='2037-01-01')),
                ('flag', models.IntegerField()),
                ('level', models.IntegerField()),
                ('main_club_id', models.IntegerField()),
                ('reg_month', models.CharField(max_length=10)),
                ('developer_id', models.IntegerField(null=True)),
                ('is_modify', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='ucs_result_table_l2',
            name='feedback',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
