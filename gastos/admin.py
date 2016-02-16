from django.contrib import admin
from .models import *

# Register your models here.


@admin.register(gastos_sucursal)
class rentaAdmin(admin.ModelAdmin):
    list_display =  ('fecha', 'nombre', 'renta', 'nomina', 'telefono_internet', 'agua_luz', 'papeleria', 'varios',)
    pass


