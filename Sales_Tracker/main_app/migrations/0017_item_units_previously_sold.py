# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-30 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0016_auto_20171116_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='units_previously_sold',
            field=models.IntegerField(default=0),
        ),
    ]