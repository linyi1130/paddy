# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 14:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0008_auto_20171212_0211'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_game_freeze_record',
            name='game_no',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]