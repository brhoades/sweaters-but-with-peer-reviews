# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-13 21:25
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('browse', '0013_merge'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='reviewcomment',
            options={'verbose_name_plural': 'Review Comments'},
        ),
        migrations.AddField(
            model_name='school',
            name='created_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
