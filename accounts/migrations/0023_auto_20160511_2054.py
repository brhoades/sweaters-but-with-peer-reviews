# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-11 20:54
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0022_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='timezone',
            field=models.CharField(default=datetime.datetime(2016, 5, 11, 20, 54, 5, 595774, tzinfo=utc), max_length=100),
        ),
    ]