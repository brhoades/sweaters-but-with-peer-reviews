# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 00:47
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20160428_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default=datetime.datetime(2016, 4, 28, 0, 47, 42, 398888, tzinfo=utc), max_length=100),
        ),
    ]