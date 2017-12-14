# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-14 04:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0025_auto_20171212_2042'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemUnitSoldDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Item')),
            ],
        ),
    ]
