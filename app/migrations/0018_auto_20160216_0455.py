# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import app.models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_auto_20160316_0314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='primerregistro',
            name='comision',
            field=models.DecimalField(verbose_name=b'comisi\xc3\xb3n', max_digits=7, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='primerregistro',
            name='municipio_delegacion',
            field=models.CharField(max_length=200, null=True, verbose_name=b'Municio o Deledaci\xc3\xb3n'),
        ),
        migrations.AlterField(
            model_name='primerregistro',
            name='numero_de_cuenta',
            field=models.CharField(max_length=16, verbose_name=b'n\xc3\xbamero de cuenta'),
        ),
        migrations.AlterField(
            model_name='primerregistro',
            name='telefono',
            field=models.PositiveIntegerField(verbose_name=b'tel\xc3\xa9fono'),
        ),
        migrations.AlterField(
            model_name='segundoregistro',
            name='caratula',
            field=models.FileField(null=True, upload_to=app.models.guardar_caratula, blank=True),
        ),
        migrations.AlterField(
            model_name='segundoregistro',
            name='credito',
            field=models.DecimalField(null=True, verbose_name=b'cr\xc3\xa9dito', max_digits=7, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='segundoregistro',
            name='ife',
            field=models.FileField(null=True, upload_to=app.models.guardar_ife, blank=True),
        ),
        migrations.AlterField(
            model_name='segundoregistro',
            name='tarjeta_de_mejoravit',
            field=models.FileField(null=True, upload_to=app.models.guardar_tarjeta, blank=True),
        ),
    ]
