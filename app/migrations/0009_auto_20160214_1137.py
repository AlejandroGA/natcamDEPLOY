# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-14 17:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_primerregistro_fecha'),
    ]

    operations = [
        migrations.AlterField(
            model_name='relacionp',
            name='cliente',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.PrimerRegistro', unique=True),
        ),
    ]
