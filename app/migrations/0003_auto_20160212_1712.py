# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-12 23:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160212_1424'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primerregistro',
            name='ife',
            field=models.FileField(upload_to='/ifes'),
        ),
        migrations.AlterField(
            model_name='segundoregistro',
            name='caratula',
            field=models.FileField(blank=True, null=True, upload_to='/caratula'),
        ),
        migrations.AlterField(
            model_name='segundoregistro',
            name='tarjeta_de_mejoravit',
            field=models.FileField(blank=True, null=True, upload_to='/targeta_infonavit'),
        ),
    ]
