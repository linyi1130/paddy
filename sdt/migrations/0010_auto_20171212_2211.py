# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-12 22:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0009_ucs_game_freeze_record_game_no'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ucs_gamerecord',
            old_name='inactivetime',
            new_name='inactive_time',
        ),
    ]
