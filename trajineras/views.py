from msilib.schema import ListView
from django.shortcuts import get_object_or_404, redirect, render
import json

from trajineras.models import *
from trajineras.forms import *

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
    ordenJSON = request.POST.get('pedido')
    
    menu = Menu.objects.filter(activo = True).order_by('nombre')

    if request.method == 'POST':
        form = OrdenTempForm(request.POST)
        aList = json.loads(ordenJSON)
        for m in aList:
            print(m['nombre'] + ' ' + m['precio'] + ' ' + m['cantidad'])

        # if form.is_valid():
        #     form.save()
        return redirect('orden_lista')
    else:
        form = OrdenTempForm()

    return render(request, 'ordenTemp/crear.html', {'form':form, 'menu':menu})