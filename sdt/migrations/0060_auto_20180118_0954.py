# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-01-18 09:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdt', '0059_auto_20180118_0921'),
    ]

    operations = [
        migrations.AddField(
            model_name='ucs_operator',
            name='developer_id',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='ucs_operator',
            name='operator_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]