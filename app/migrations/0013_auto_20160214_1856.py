# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-15 00:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_relacionp_crbd_rpago'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relacionp',
            name='crbd_rpago',
            field=models.BooleanField(default=False),
        ),
    ]
