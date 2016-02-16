# coding=utf-8
from django.shortcuts import render,redirect, get_object_or_404
from forms import *
from models import *
from usuarios.models import Datos, Sucursal
from django.http import HttpResponseRedirect
import datetime



#Gastos de renta
def renta(request):

    gastosEnero = gastos_sucursal.objects.filter(fecha__month=1).filter(fecha__year=2016)
    gastosFebrero = gastos_sucursal.objects.filter(fecha__month=2).filter(fecha__year=2016)
    gastosMarzo = gastos_sucursal.objects.filter(fecha__month=3).filter(fecha__year=2016)
    gastosAbril = gastos_sucursal.objects.filter(fecha__month=4).filter(fecha__year=2016)
    gastosMayo = gastos_sucursal.objects.filter(fecha__month=5).filter(fecha__year=2016)
    gastosJunio = gastos_sucursal.objects.filter(fecha__month=6).filter(fecha__year=2016)
    gastosJulio = gastos_sucursal.objects.filter(fecha__month=7).filter(fecha__year=2016)
    gastosAgosto = gastos_sucursal.objects.filter(fecha__month=8).filter(fecha__year=2016)
    gastosSeptiembre = gastos_sucursal.objects.filter(fecha__month=9).filter(fecha__year=2016)
    gastosOctubre = gastos_sucursal.objects.filter(fecha__month=10).filter(fecha__year=2016)
    gastosNoviembre = gastos_sucursal.objects.filter(fecha__month=11).filter(fecha__year=2016)
    gastosDiciembre = gastos_sucursal.objects.filter(fecha__month=12).filter(fecha__year=2016)


    if request.method == 'POST':
        form = gastosForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/asesor/gastos_sucursal/')
    else:
            form = gastosForm()
    sucursal = Sucursal.objects.all()
    operadort = request.user
    datos = Datos.objects.get(usuario = operadort)
    gastos = gastos_sucursal.objects.all().first()
    return render(request, 'asesor/gastos_sucursal.html', {'form': form,
                                                           'gastosEnero':gastosEnero,
                                                           'gastosFebrero':gastosFebrero,
                                                           'gastosMarzo':gastosMarzo,
                                                           'gastosAbril':gastosAbril,
                                                           'gastosMayo':gastosMayo,
                                                           'gastosJunio':gastosJunio,
                                                           'gastosJulio':gastosJulio,
                                                           'gastosAgosto':gastosAgosto,
                                                           'gastosSeptiembre':gastosSeptiembre,
                                                           'gastosOctubre':gastosOctubre,
                                                           'gastosNoviembre':gastosNoviembre,
                                                           'gastosDiciembre':gastosDiciembre,
                                                           'sucursal':sucursal,
                                                           'datos':datos,
                                                           'gastos':gastos,
                                                           })

def GastosEdit(request, pk, template_name='asesor/editar_gastos.html'):
    gastos = get_object_or_404(gastos_sucursal, pk=pk)
    form = gastosForm(request.POST or None, instance=gastos)
    if form.is_valid():
        form.save()
        return redirect('gasto_sucursal')
    return render(request, template_name, {'form': form})
