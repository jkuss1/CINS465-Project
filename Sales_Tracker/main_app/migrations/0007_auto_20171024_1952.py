# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 02:52
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_auto_20171024_1945'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='dateUpdated',
            new_name='dateLastUpdated',
        ),
    ]
