# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-28 00:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0017_auto_20160428_0024'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Settings',
        ),
    ]
