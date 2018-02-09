# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-13 22:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0012_auto_20171213_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_game_freeze_record',
            name='status',
            field=models.CharField(default='预占用', max_length=10),
        ),
        migrations.AddField(
            model_name='ucs_game_freeze_record',
            name='unfreeze_time',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
