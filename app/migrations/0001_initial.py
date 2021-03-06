# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-12 18:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden_compra', models.CharField(choices=[('1', 'Orden de Compra 1'), ('2', 'Orden de Compra 2'), ('3', 'Orden de Compra 3')], max_length=1, verbose_name='orden de compra')),
                ('order_date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('operador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrimerRegistro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=55)),
                ('apellidos', models.CharField(max_length=80)),
                ('calle', models.CharField(max_length=80, null=True)),
                ('numero', models.CharField(max_length=20, null=True)),
                ('colonia_fraccionamiento', models.CharField(max_length=200, null=True, verbose_name='Colonia o Fraccionamiento')),
                ('municipio_delegacion', models.CharField(max_length=200, null=True, verbose_name='Municio o Deledación')),
                ('endidad', models.CharField(max_length=50, null=True)),
                ('cp', models.CharField(max_length=20, null=True)),
                ('nss', models.CharField(max_length=11, null=True, verbose_name='nss')),
                ('telefono', models.PositiveIntegerField(verbose_name='teléfono')),
                ('empresa', models.CharField(max_length=254)),
                ('registro_patronal', models.CharField(max_length=15)),
                ('comision', models.DecimalField(decimal_places=2, max_digits=7, verbose_name='comisión')),
                ('ife', models.FileField(upload_to='media/ifes')),
                ('email', models.EmailField(max_length=254)),
                ('numero_de_cuenta', models.CharField(max_length=16, verbose_name='número de cuenta')),
                ('banco', models.CharField(max_length=15)),
                ('operador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Primer Registro',
            },
        ),
        migrations.CreateModel(
            name='ProductOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Order')),
            ],
        ),
        migrations.CreateModel(
            name='Productos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Productos',
                'verbose_name_plural': 'Productos',
            },
        ),
        migrations.CreateModel(
            name='RelacionP',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField(default=django.utils.timezone.now)),
                ('odc1', models.PositiveIntegerField()),
                ('odc2', models.PositiveIntegerField()),
                ('odc3', models.PositiveIntegerField()),
                ('pag_clie', models.PositiveIntegerField()),
                ('p_asesor', models.PositiveIntegerField()),
                ('comision', models.PositiveIntegerField()),
                ('com_t', models.PositiveIntegerField()),
                ('ref_pago', models.CharField(max_length=20, null=True, verbose_name='Referencia de Pago')),
                ('importe', models.DecimalField(decimal_places=2, max_digits=7, null=True, verbose_name='Importe')),
                ('asesor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cliente', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.PrimerRegistro')),
            ],
        ),
        migrations.CreateModel(
            name='SegundoRegistro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('caratula', models.FileField(blank=True, null=True, upload_to='media/caratula')),
                ('tarjeta_de_mejoravit', models.FileField(blank=True, null=True, upload_to='media/targeta_infonavit')),
                ('credito', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='crédito')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.PrimerRegistro')),
                ('operador', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Segundo Registro',
            },
        ),
        migrations.CreateModel(
            name='TercerRegistro',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('compra', models.TextField()),
                ('importe_total', models.DecimalField(decimal_places=2, max_digits=10)),
                ('efectivo', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comision', models.DecimalField(decimal_places=2, max_digits=10)),
                ('fecha', models.DateField(auto_now_add=True)),
                ('numero_credito', models.CharField(max_length=10)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.PrimerRegistro')),
            ],
            options={
                'verbose_name_plural': 'Tercer Registro',
            },
        ),
        migrations.AddField(
            model_name='productorder',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Productos'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.PrimerRegistro'),
        ),
    ]
