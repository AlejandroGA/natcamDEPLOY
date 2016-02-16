# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_sucursal_color'),
    ]

    operations = [
        migrations.CreateModel(
            name='gastos_sucursal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fecha', models.DateField(verbose_name=datetime.datetime(2016, 2, 16, 4, 55, 34, 767000))),
                ('nombre', models.CharField(max_length=60)),
                ('renta', models.DecimalField(max_digits=7, decimal_places=2)),
                ('nomina', models.DecimalField(max_digits=7, decimal_places=2)),
                ('telefono_internet', models.SmallIntegerField()),
                ('agua_luz', models.DecimalField(max_digits=7, decimal_places=2)),
                ('papeleria', models.DecimalField(max_digits=7, decimal_places=2)),
                ('varios', models.DecimalField(max_digits=7, decimal_places=2)),
                ('sucursal', models.ForeignKey(to='usuarios.Sucursal', null=True)),
            ],
            options={
                'verbose_name_plural': 'Gastos Sucursal',
            },
        ),
    ]
