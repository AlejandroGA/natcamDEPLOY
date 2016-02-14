from itertools import chain
from django.core.mail import send_mail
from django.db.models import Q
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from .forms import PrimerRegistroFORM, SegundoRegistroForm, OrderForm, EmailOdcsForm, CargarPdfsForm
from django.http import HttpResponseRedirect
from .models import PrimerRegistro, SegundoRegistro, Productos, ProductOrder, Order, RelacionP
#from users.models import User
from django.contrib.auth.decorators import login_required
from  django.core import serializers
import json
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from usuarios.models import Datos, Sucursal


def index(request):
    return render(request, 'index.html', )



#@login_required(login_url='/')
def clientes(request):
    usuario = request.user
    if request.method == 'POST':
        form = SegundoRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            cliente = form.cleaned_data['cliente']
            ife = form.cleaned_data['ife']
            caratula = form.cleaned_data['caratula']
            tarjeta = form.cleaned_data['tarjeta_de_mejoravit']
            credito = form.cleaned_data['credito']
            getcliente = PrimerRegistro.objects.get(id = cliente)
            operador = form.operador = getcliente.operador

            ar = SegundoRegistro.objects.create(cliente=getcliente, ife=ife,caratula=caratula, tarjeta_de_mejoravit=tarjeta,credito=credito , operador=operador)
            ar.save()
            return redirect('desempeno')
    else:
        form = SegundoRegistroForm()
    datos = Datos.objects.get(usuario=usuario)
    sucursa = datos.sucursal
    asesores = Datos.objects.filter(sucursal=sucursa)
    for ase in asesores:
        cliente = PrimerRegistro.objects.filter(operador__username__contains=ase)
        tarjeta = SegundoRegistro.objects.filter(operador__username__contains=ase)
        ordenes = Order.objects.filter(operador__username__contains=ase)
        orden1 = Order.objects.filter(Q(orden_compra="1") & Q(operador__username__contains=ase))
        orden2 = Order.objects.filter(Q(orden_compra="2") & Q(operador__username__contains=ase))
        orden3 = Order.objects.filter(Q(orden_compra="3") & Q(operador__username__contains=ase))
        odcs = Order.objects.filter(Q(operador__username__contains=usuario))
        return render(request, 'clientes.html', {
            'cliente': cliente,
            'tarjeta': tarjeta,
            'ordenes': ordenes,
            'orden1': orden1,
            'orden2': orden2,
            'orden3': orden3,
            'odcs': odcs,
            'form':form,
            'datos':datos
        })

#@login_required(login_url='/')
def desempeno(request):
    usuario = request.user
    datos = Datos.objects.get(usuario = usuario)
    if datos.tipo == "1":
        mi_info = User.objects.get(username=usuario)
        total_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario).count()
        micomision = PrimerRegistro.objects.filter(operador__username__contains=usuario)
        micomiscionAsesor = SegundoRegistro.objects.filter(operador__username__contains=usuario)
        #percepcion = SegundoRegistro.objects.filter(operador__username__contains=usuario).aggregate(Sum('micomision'))
        return render(request, 'asesor/desempeno.html', {'mi_info': mi_info,
                                                  'total_clientes': total_clientes,
                                                  'micomision':micomision,
                                                  'micomiscionAsesor':micomiscionAsesor,
                                                  })
    elif datos.tipo == "2":
        mi_info = User.objects.get(username=usuario)
        total_clientes = PrimerRegistro.objects.filter(operador__username__contains=usuario).count()
        micomision = PrimerRegistro.objects.filter(operador__username__contains=usuario)
        micomiscionAsesor = SegundoRegistro.objects.filter(operador__username__contains=usuario)
        #percepcion = SegundoRegistro.objects.filter(operador__username__contains=usuario).aggregate(Sum('micomision'))
        return render(request, 'asistente/desempeno.html', {'mi_info': mi_info,
                                                  'total_clientes': total_clientes,
                                                  'micomision':micomision,
                                                  'micomiscionAsesor':micomiscionAsesor,
                                                  #'percepcion': percepcion
                                                  })

#@login_required(login_url='/')
def primerRegistro(request):
    operadort = request.user
    datos = Datos.objects.get(usuario = operadort)

    if datos.tipo == "1":
        sucursal = datos.sucursal
        sacar_asesor = Datos.objects.get(Q(tipo = '2')& Q(sucursal=sucursal))
        odcs = Order.objects.filter(Q(operador__username__contains=sacar_asesor.usuario))
        ordenes = Order.objects.filter(operador__username__contains=operadort)
        orden1 = Order.objects.filter(Q(orden_compra="1") & Q(operador=sacar_asesor.usuario ))
        orden2 = Order.objects.filter(Q(orden_compra="2") & Q(operador=sacar_asesor.usuario))
        orden3 = Order.objects.filter(Q(orden_compra="3") & Q(operador=sacar_asesor.usuario))
        datos = Datos.objects.get(usuario = operadort)
        if request.method == 'POST':
            form = PrimerRegistroFORM(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.operador = operadort
                post.save()
                return redirect('agregar_clientes')
        else:
            form = PrimerRegistroFORM()
        mis_clientes = PrimerRegistro.objects.filter(operador__username__contains=operadort)
        return render(request, 'asesor/index.html', {
                                              'form': form,
                                              'mis_clientes': mis_clientes,
                                              'odcs': odcs,
                                              'orden1':orden1,
                                              'orden2':orden2,
                                              'orden3':orden3,
                                               'datos':datos })
    elif datos.tipo == "2":
        return redirect('clientes')
    elif datos.tipo == "3":
        return redirect('calendario')



#@login_required(login_url='/')
def PrimerRegistroEdit(request, pk, template_name='editar/primer_registro.html'):
    clientes = get_object_or_404(PrimerRegistro, pk=pk)
    form = PrimerRegistroFORM(request.POST or None, instance=clientes)
    if form.is_valid():
        form.save()
        return redirect('agregar_clientes')
    return render(request, template_name, {'form': form})


#@login_required(login_url='/')
def PrimerRegistroDelete(request, pk, template_name='delete/confirmacion.html'):
    clientes = get_object_or_404(PrimerRegistro, pk=pk)
    if request.method == 'POST':
        clientes.delete()
        return redirect('agregar_clientes')
    return render(request, template_name, {'object': clientes})


#@login_required(login_url='/')
def segundoRegistro(request):
    usuario = request.user
    if request.method == 'POST':
        form = SegundoRegistroForm(request.POST, request.FILES)
        if form.is_valid():
            posta = form.save(commit=False)
            posta.operador = usuario
            posta.save()
            return redirect('segundo_registro')
    else:
        form = SegundoRegistroForm()
    mis_clientes = SegundoRegistro.objects.filter(operador__username__contains=usuario)
    return render(request, 'segundo-registro.html', {'form': form, 'mis_clientes': mis_clientes})

#@login_required(login_url='/')
def SegundoRegistroEdit(request, pk, template_name='editar/segundo_registro.html'):
    clientes = get_object_or_404(SegundoRegistro, pk=pk)
    form = SegundoRegistroForm(request.POST or None, instance=clientes)
    if form.is_valid():
        form.save()
        return redirect('segundo_registro')
    return render(request, template_name, {'form': form})

#@login_required(login_url='/')
def SegundoRegistroDelete(request, pk, template_name='delete/confirmacion2.html'):
    clientes = get_object_or_404(SegundoRegistro, pk=pk)
    if request.method == 'POST':
        clientes.delete()
        return redirect('segundo_registro')
    return render(request, template_name, {'object': clientes})

#@login_required(login_url='/')
def orden_compra1(request, cliente_id=None):
    # data = serializers.serialize("json", Productos.objects.all(), fields=('pk', 'name', 'price'))
    if Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=1)).exists():
        ordencliente = Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=1))
        productos = ProductOrder.objects.filter(order=ordencliente)
        return render(request, 'odc/odc1-echa.html', {'ordencliente': ordencliente,
                                                      'productos': productos})
    else:
        cliente = get_object_or_404(PrimerRegistro, id=cliente_id)
        productos = Productos.objects.all()
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                user = cliente
                order_content = json.loads(request.POST['cartJSONdata'])
                order = form.save(commit=False)
                order.user = user
                order.operador = request.user
                order.total_amount = 0
                order.save()  # We have to save the order before calculate ammount
                order.total_amount = saveOrderProducts(order_content, order)
                order.save()
                books = ProductOrder.objects.filter(order=order)
                products = list(chain(books, ))
                return redirect('/clientes')
                # return render(request, 'success.html', locals())
        else:
            form = OrderForm()
        # lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
        # serializado = json.dumps(lista)
        return render(request, 'odc/odc1.html', {'productos': productos,
                                                 'cliente': cliente,
                                                 'form': form,
                                                 # 'data':data,
                                                 # 'lista':serializado,
                                                 })

#@login_required(login_url='/')
def orden_compra2(request, cliente_id=None):
    if Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=2)).exists():
        ordencliente = Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=2))
        productos = ProductOrder.objects.filter(order=ordencliente)
        return render(request, 'odc/odc1-echa.html', {'ordencliente': ordencliente,
                                                      'productos': productos})

    else:
        cliente = get_object_or_404(PrimerRegistro, id=cliente_id)
        productos = Productos.objects.all()
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                user = cliente
                order_content = json.loads(request.POST['cartJSONdata'])
                order = form.save(commit=False)
                order.user = user
                order.operador = request.user
                order.total_amount = 0
                order.save()  # We have to save the order before calculate ammount
                order.total_amount = saveOrderProducts(order_content, order)
                order.save()
                books = ProductOrder.objects.filter(order=order)
                products = list(chain(books, ))
                return redirect('clientes')
                # return render(request, 'success.html', locals())
        else:
            form = OrderForm()
        # lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
        # serializado = json.dumps(lista)
        return render(request, 'odc/odc2.html', {'productos': productos,
                                                 'cliente': cliente,
                                                 'form': form,
                                                 # 'data':data,
                                                 # 'lista':serializado,
                                                 })

#@login_required(login_url='/')
def orden_compra3(request, cliente_id=None):
    if Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=3)).exists():
        ordencliente = Order.objects.filter(Q(user__id=cliente_id) & Q(orden_compra=2))
        productos = ProductOrder.objects.filter(order=ordencliente)
        return render(request, 'odc/odc1-echa.html', {'ordencliente': ordencliente,
                                                      'productos': productos})
    else:
        cliente = get_object_or_404(PrimerRegistro, id=cliente_id)
        productos = Productos.objects.all()
        if request.method == "POST":
            form = OrderForm(request.POST)
            if form.is_valid():
                user = cliente
                order_content = json.loads(request.POST['cartJSONdata'])
                order = form.save(commit=False)
                order.user = user
                order.operador = request.user
                order.total_amount = 0
                order.save()  # We have to save the order before calculate ammount
                order.total_amount = saveOrderProducts(order_content, order)
                order.save()
                books = ProductOrder.objects.filter(order=order)
                products = list(chain(books, ))
                return redirect('clientes')
                # return render(request, 'success.html', locals())
        else:
            form = OrderForm()
        # lista = [{'pk':producto.pk, 'name':producto.nombre, 'price': Decimal(producto.precio), } for producto in productos]
        # serializado = json.dumps(lista)
        return render(request, 'odc/odc3.html', {'productos': productos,
                                                 'cliente': cliente,
                                                 'form': form,
                                                 # 'data':data,
                                                 # 'lista':serializado,
                                                 })
def saveOrderProducts(order_content, order):
    amount = 0
    prod_error = False
    for product in order_content:
        product_uid = product['id']
        quantity = product['quantity']
        p_price = product['price']
        amount += float(p_price) * float(quantity)
        product_obj = Productos.objects.get(pk=product_uid)
        product_obj.save()
        prod_order = order.productorder_set.create(product=product_obj, quantity=quantity)

        if not prod_error:
            prod_order.save()
    return amount

from django.db.models import Sum

def enviar_email(request, cliente_id=None):
    posta = Order.objects.filter(user=cliente_id).aggregate(Sum('total_amount'))
    post = Order.objects.filter(user=cliente_id)
    primerr = PrimerRegistro.objects.get(id = cliente_id)
    sent = False
    if request.method == 'POST':
        form = EmailOdcsForm(request.POST)
        if form.is_valid():
            enviaryael(request,cliente_id)
            cd = form.cleaned_data
            allorder = [(p.total_amount) for p in Order.objects.filter(user=cliente_id)]
            if len(allorder) == 3:
                subject = '  recommends you reading '
                message = 'Cliente Listo \n\n\'s  datos Orden 1:{}\n\n Orden 2:{}\n\n Orden 3: {}\n\n Total:{}  comments: {} '.format(allorder[0], allorder[1], allorder[2], posta['total_amount__sum'], cd['comments'], )
                #message.attach('ife')
                send_mail(subject, message, 'soldiddfouns@gmail.com', [cd['to']])
                sent = True
                redirect('clientes')
            elif len(allorder) == 2:
                subject = '  recommends you reading '
                message = 'Cliente Listo \n\n\'s  datos Orden 1:{}\n\n Orden 2:{}\n\n  Total:{}  comments: {} '.format(allorder[0], allorder[1], posta['total_amount__sum'], cd['comments'], )
                #message.attach('ife')
                send_mail(subject, message, 'soldiddfouns@gmail.com', [cd['to']])
                sent = True
                redirect('clientes')

        else:
            return redirect('clientes')
    else:

        form = EmailOdcsForm()
        #formr =RelacionPFprm()
    return render(request, 'enviar.html', {'post': post,
                                           'posta': posta,
                                           'form': form,
                                           'sent': sent,
                                           #'formr':formr
                                           })

#def enviaryael(request,fecha, cliente, odc1,odc2,odc3 ,pag_clie ,p_asesor,comision,com_t,asesor,ref_pago, importe):
def enviaryael(request, cliente_id):
    contars3 =Order.objects.filter(user__id =cliente_id, orden_compra__contains =3)
    if contars3.count() > 0:
        infocliente  = PrimerRegistro.objects.get(id=cliente_id)
        segundor = SegundoRegistro.objects.get(cliente__id=cliente_id)
        odc1 = Order.objects.get(user__id =cliente_id, orden_compra__contains =1)
        od1 = float(odc1.total_amount)
        odc2 = Order.objects.get(user__id =cliente_id, orden_compra__contains =2)
        od2 = float(odc2.total_amount)
        odc3 = Order.objects.get(user__id =cliente_id, orden_compra__contains =3)
        od3 = float(odc3.total_amount)
        totalodc = Order.objects.filter(user__id=cliente_id).aggregate(Sum('total_amount'))
        totalodcs = float(totalodc['total_amount__sum'])
        comision = infocliente.comision
        com = float(comision)
        p_comision = segundor.comisiona()
        pcom = float(p_comision)
        suma = com + pcom
        sumaimporte = totalodcs -suma
        nombre = infocliente.id
        o_cliente = PrimerRegistro.objects.get(id=nombre)
        fecha = timezone.now()
        form = RelacionP.objects.create(
                    fecha = fecha,
                    cliente =  o_cliente,
                    odc1 = od1,
                    odc2 = od2,
                    odc3 = od3,
                    pag_clie = totalodcs,
                    p_asesor = pcom ,
                    comision = com,
                    com_t = suma,
                    asesor = request.user,
                    # ref_pago = request.POST['ref_pago'],
                    importe = sumaimporte,
                )
    else:
        infocliente  = PrimerRegistro.objects.get(id=cliente_id)
        segundor = SegundoRegistro.objects.get(id=cliente_id)
        odc1 = Order.objects.get(user__id =cliente_id, orden_compra__contains =1)
        od1 = float(odc1.total_amount)
        odc2 = Order.objects.get(user__id =cliente_id, orden_compra__contains =2)
        od2 = float(odc2.total_amount)
        totalodc = Order.objects.filter(user__id=cliente_id).aggregate(Sum('total_amount'))
        totalodcs = float(totalodc['total_amount__sum'])
        comision = infocliente.comision
        com = float(comision)
        p_comision = segundor.comisiona()
        pcom = float(p_comision)
        suma = com + pcom
        sumaimporte = totalodcs -suma
        nombre = infocliente.id
        o_cliente = PrimerRegistro.objects.get(id=nombre)
        fecha = timezone.now()
        form = RelacionP.objects.create(
                    fecha = fecha,
                    cliente =  o_cliente,
                    odc1 = od1,
                    odc2 = od2,
                    pag_clie = totalodcs,
                    p_asesor = pcom ,
                    comision = com,
                    com_t = suma,
                    asesor = request.user,
                    # ref_pago = request.POST['ref_pago'],
                    importe = sumaimporte,
                )
        return redirect('clientes')

def dia(request, year, month, day):
    #form = RelacionPFprm()
    diass =  get_list_or_404(RelacionP, fecha__year=year,
                                        fecha__month=month,
                                        fecha__day=day,)
    return render(request, 'gaeladmin/dia.html', {
                                                    #'form': form,
                                                   'diass':diass
                                                  })


from calendar import HTMLCalendar
from datetime import date
from  itertools import groupby
from  django.utils.html import conditional_escape as esc
from .forms import BuscarDiaForm
def calendario(request):
    if request.method == 'POST':
        form = BuscarDiaForm(request.POST)
        if form.is_valid():
             fetch = form.cleaned_data['fecha']
             year = fetch.year
             month = fetch.month
             day = fetch.day
             return dia(request, year, month, day)
    else:
        form = BuscarDiaForm()
    diass = RelacionP.objects.all()
    return render(request, 'gaeladmin/calendar.html', {'form':form,
                                                       'diass':diass})

def cargar_pdfs(request, id):
    form = CargarPdfsForm
    return render(request, 'cargar-pdf/cargar-pdfs.html', {'form':form})


def cliente_perfil(request, id):
    obtenerClientePR = PrimerRegistro.objects.get(id=id)
    #obtenerClienteSR = SegundoRegistro.objects.get()
    return render(request, 'perfil/peril-cliente.html', {
                                                    'primer':obtenerClientePR,
                                                    #'segundo'
    })

def sucursales(request):
    datosusuarios = Datos.objects.all()
    sucursales = Sucursal.objects.all()
    return render(request, 'gaeladmin/sucursales.html', {
                                                        'datos':datosusuarios,
                                                        'sucursales': sucursales,
    })

def gastos_oficina(request):
    return  render(request,'asistente/gastos-oficina.html')

def empleado_perfil(request, id):
    obtenerEmpleado = Datos.objects.get(id=id)
    return render(request, 'perfil/perfil-empleado.html',{'primer':obtenerEmpleado,})