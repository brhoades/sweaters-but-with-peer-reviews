# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-03 20:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0005_auto_20160203_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
