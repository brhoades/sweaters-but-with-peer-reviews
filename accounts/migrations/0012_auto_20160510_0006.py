# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-10 00:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20160506_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default=datetime.datetime(2016, 5, 10, 0, 6, 46, 750943, tzinfo=utc), max_length=100),
        ),
    ]
