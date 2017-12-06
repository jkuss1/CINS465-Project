# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 02:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_auto_20171024_1917'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='dateAdded',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='item',
            name='dateUpdated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
