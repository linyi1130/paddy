# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-02-06 20:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0079_ucs_game_reward_club_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_club_user',
            name='feedback',
            field=models.IntegerField(default=0),
        ),
    ]
