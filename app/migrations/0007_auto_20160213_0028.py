# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-13 06:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160212_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relacionp',
            name='odc2',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='relacionp',
            name='odc3',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
