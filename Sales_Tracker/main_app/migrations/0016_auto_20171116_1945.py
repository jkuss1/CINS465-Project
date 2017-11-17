# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-17 03:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0015_item_units_purchased'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='cost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=12),
        ),
    ]
