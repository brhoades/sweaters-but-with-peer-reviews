# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-03 21:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0006_course_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='text',
            field=models.TextField(default='', max_length=100000),
            preserve_default=False,
        ),
    ]
