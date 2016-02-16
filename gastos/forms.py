from django import forms
from .models import *
from django.forms import ModelForm



class gastosForm(ModelForm):
     class Meta:
         model = gastos_sucursal
         fields = ('fecha', 'nombre', 'renta', 'nomina', 'telefono_internet', 'agua_luz', 'papeleria', 'varios',)

