# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-21 03:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0015_log_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='summary',
            field=models.TextField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
