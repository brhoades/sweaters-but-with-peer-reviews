# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-11 21:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_auto_20160511_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default=datetime.datetime(2016, 5, 11, 21, 55, 28, 936620, tzinfo=utc), max_length=100),
        ),
    ]
