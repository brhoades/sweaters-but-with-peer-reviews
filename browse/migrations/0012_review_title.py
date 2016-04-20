# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-04 21:34
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browse', '0011_auto_20160316_0257'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.TextField(default='Default Title', max_length=100, validators=[django.core.validators.MinLengthValidator(3)]),
            preserve_default=False,
        ),
    ]