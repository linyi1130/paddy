# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-29 17:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0077_ucs_game_reward_record'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ucs_game_reward_record',
            name='blind_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ucs_game_reward_record',
            name='type_id',
            field=models.IntegerField(null=True),
        ),
    ]