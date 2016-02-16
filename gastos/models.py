from __future__ import unicode_literals
from time import timezone
from usuarios.models import Sucursal

from django.db import models
from datetime import datetime

# Create your models here.

class gastos_sucursal(models.Model):
    sucursal = models.ForeignKey(Sucursal, null=True)
    fecha = models.DateField(datetime.now())
    nombre = models.CharField(max_length=60)
    renta = models.DecimalField(max_digits=7, decimal_places=2)
    nomina= models.DecimalField(max_digits=7, decimal_places=2)
    telefono_internet = models.SmallIntegerField()
    agua_luz = models.DecimalField(max_digits=7, decimal_places=2)
    papeleria = models.DecimalField(max_digits=7, decimal_places=2)
    varios = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        verbose_name_plural = 'Gastos Sucursal'

    def __str__(self):
        return self.nombre


