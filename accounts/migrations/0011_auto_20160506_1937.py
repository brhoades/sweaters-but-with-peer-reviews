# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-06 19:37
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160504_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default=datetime.datetime(2016, 5, 6, 19, 37, 24, 199556, tzinfo=utc), max_length=100),
        ),
    ]