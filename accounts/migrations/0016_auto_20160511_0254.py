# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-11 02:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_auto_20160510_2258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default=datetime.datetime(2016, 5, 11, 2, 54, 6, 918876, tzinfo=utc), max_length=100),
        ),
    ]