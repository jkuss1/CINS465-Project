# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-01 06:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0018_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='itemIDs',
            field=models.TextField(max_length=1000),
        ),
    ]
