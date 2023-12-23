import decimal
from msilib.schema import ListView
from django.shortcuts import get_object_or_404, redirect, render
import json

from trajineras.models import *
from trajineras.forms import *

def index(request):
    return render(request, 'index.html')

# MENU ==============================================================================================================================
#====================================================================================================================================

def ListadoMenu(request): # LISATDO -------------------------------------------------------------------------
    menu = Menu.objects.filter(activo = True).order_by('id')

    return render(request,'menu/lista.html', {'menu' : menu})

def CrearMenu(request): # CRREAR ----------------------------------------------------------------------------

    data = { 'form' : MenuForm() }

    if request.method == 'POST':
        formulario=MenuForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="menu_lista")
        else:
            data['form'] = formulario
    return render(request, 'menu/crear.html',data)

def EditarMenu(request, pk): # EDITAR ------------------------------------------------------------------------

    menu = get_object_or_404(Menu, id = pk)
    data = { 'form' : MenuForm(instance = menu) }

    if request.method == 'POST':
        formulario = MenuForm(data = request.POST, instance = menu)
        if formulario.is_valid():
            formulario.save()
            return redirect('menu_lista')
        data['form'] = formulario
    return render(request, 'menu/crear.html', data)

def BorrarMenu(request, pk): # ELIMINAR ----------------------------------------------------------------------
    menu = get_object_or_404(Menu, id = pk)
    menu.delete()
    return redirect('menu_lista')


# ORDENES TEMPORALES ================================================================================================================
#====================================================================================================================================

def ListadoOrdenTemp(request): # LISATDO -----------------------------------------------------------------------
    ordenesTemp = OrdenTemp.objects.all().order_by('id')

    return render(request,'ordenTemp/lista.html', {'ordenes' : ordenesTemp})

def CrearOrdenTemp(request): # CRREAR ----------------------------------------------------------------------------
    menu = Menu.objects.filter(activo = True).order_by('nombre')

    if request.method == 'POST':
        form = OrdenTempForm(request.POST)
        
        pedidoJSON = request.POST.get('pedido') 
        if pedidoJSON:
            pedidoDicc = json.loads(pedidoJSON) # Diccionario con la orden convertida desde el JSON
        else:
            form = OrdenTempForm()
        
        total = 0.0 # Acumulador del total de la orden

        if form.is_valid():
            orderForm = form.save(commit=False)

            for pedido in pedidoDicc:
                total += (float(pedido['precio']) * int(pedido['cantidad']))
           
            orderForm.total = total
            orderForm.save()
            orderId = orderForm.id # ID de la orden recien creada

            # Guardar el contenido inicial de la orden
            for p in pedidoDicc:
                form2 = OrdenMenuForm()
                contOrden = form2.save(commit=False) 
                contOrden.idOrden = orderId
                contOrden.idMenu = int(p['id'])
                contOrden.cantidad = int(p['cantidad'])
                contOrden.save()

            return redirect('orden_lista')
        else:
            form = OrdenTempForm()
    
    else:
        form = OrdenTempForm()
 
    return render(request, 'ordenTemp/crear.html', {'form':form, 'menu':menu})

def DetalleOrdenTemp(request): # DETALLE ------------------------------------------------------------------------
    pk = request.GET.get('id') # que viene del AJAX
    orden = get_object_or_404(OrdenTemp, id = pk)  
    content = getOrderDetail(pk)

    return render(request, 'ordenTemp/detalle.html', {'orden': orden, 'contOrden': content})

def AgregarContenido(request, pk): # AGREGAR COSAS AL PEDIDO -------------------------------------------------------
    orden = get_object_or_404(OrdenTemp, id = pk)  
    contenidoActual = getOrderDetail(pk)
    menu = Menu.objects.filter(activo = True).order_by('nombre')

    if request.method == 'POST':
        total = 0.0

        pedidoJSON = request.POST.get('pedido') 
        if pedidoJSON:
            pedidoDicc = json.loads(pedidoJSON) # Diccionario con la orden convertida desde el JSON
        else:
            return render(request, 'ordenTemp/agregar.html', {'orden': orden, 'currContent': contenidoActual, 'menu': menu})

        for pedido in pedidoDicc:
                total += (float(pedido['precio']) * int(pedido['cantidad']))

        # Guardar el contenido inicial de la orden
        for p in pedidoDicc:
            form2 = OrdenMenuForm()
            contOrden = form2.save(commit=False) 
            contOrden.idOrden = orden.id
            contOrden.idMenu = int(p['id'])
            contOrden.cantidad = int(p['cantidad'])
            contOrden.nuevo = True # Es de los agregados depues
            contOrden.save()

        orden.total = orden.total + decimal.Decimal(total) # Actualizar el total de la orden
        orden.save()
        return redirect('orden_lista')

    return render(request, 'ordenTemp/agregar.html', {'orden': orden, 'currContent': contenidoActual, 'menu': menu})

def BorrarOrdenTemp(request, pk): # ELIMINAR ----------------------------------------------------------------------
    orden = get_object_or_404(OrdenTemp, id = pk)
    OrdenMenu.objects.filter(idOrden = orden.id).delete()
    orden.delete()
    return redirect('orden_lista')
  

# Obtener el contenido de una orden temporal específica===========================================================
def getOrderDetail(id): 
    ordenMenu = OrdenMenu.objects.filter(idOrden = id) # ID's de los contenidos de la orden

    contOrden = OrdenMenu.objects.none()
    content = []
    for oId in ordenMenu:
        contOrden = Menu.objects.filter(id = oId.idMenu).first()
        item = {'id':contOrden.id, 'nombre':contOrden.nombre, 'precio': contOrden.precio, 'cantidad': oId.cantidad, 'nuevo': oId.nuevo}
        content.append(item)

    return (content)

# ORDENES PERMANENTES (HISTÓRICO) ===================================================================================================
#====================================================================================================================================