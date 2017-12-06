# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 03:56
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import main_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_auto_20171024_1952'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=main_app.models.UserDirectoryPath)),
                ('desc', models.CharField(max_length=32)),
            ],
        ),
        migrations.RenameField(
            model_name='item',
            old_name='dateAdded',
            new_name='dateCreated',
        ),
        migrations.RenameField(
            model_name='item',
            old_name='dateLastUpdated',
            new_name='dateUpdated',
        ),
        migrations.RemoveField(
            model_name='item',
            name='img',
        ),
        migrations.RemoveField(
            model_name='item',
            name='imgDesc',
        ),
        migrations.AddField(
            model_name='item',
            name='cost',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='item',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='itemimage',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.Item'),
        ),
    ]
