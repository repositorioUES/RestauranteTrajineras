import decimal
from msilib.schema import ListView
from django.shortcuts import get_object_or_404, redirect, render
import json
from django.db.models import Q

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

def getMenuByType(request): # LISTAR MENU POR TIPO DE PRODUCTO -----------------------------------------------
    tipo = request.GET.get('tipo') # que viene del AJAX
    menu = Menu.objects.filter(activo = True).filter(tipo = tipo).order_by('nombre')

    return render(request, 'menu/por_tipo.html', {'menu': menu, 'tipo': tipo})


# COMANDAS ==========================================================================================================================
#====================================================================================================================================

def ListadoOrdenTemp(request): # LISATDO -----------------------------------------------------------------------
    allComandas = Comanda.objects.all().order_by('id')

    comandas = []

    for c in allComandas:
        tieneCocina = 0
        tieneBebida = 0

        co = Orden.objects.filter(Q(comanda_id = c.id) & Q(cocina__gte = 2)).exists()
        if co == True:
            tieneCocina = 2

        cocina = Orden.objects.filter(Q(comanda_id = c.id) & Q(cocina = 1)).exists()
        if cocina == True:
            tieneCocina = 1

        b = Orden.objects.filter(Q(comanda_id = c.id) & Q(bebida__gte = 2)).exists()
        if b == True:
            tieneBebida = 2

        bebida = Orden.objects.filter(Q(comanda_id = c.id) & Q(bebida = 1)).exists()
        if bebida == True:
            tieneBebida = 1
        
        item = {'id': c.id, 'mesa': c.mesa, 'fechaHora': c.fechaHora, 'total': c.total, 'cocina':tieneCocina, 'bebida': tieneBebida, 'cobrable': c.cobrable}
        comandas.append(item)

    return render(request,'comanda/lista.html', {'comandas' : comandas})

def CrearOrdenTemp(request): # CRREAR ----------------------------------------------------------------------------

    if request.method == 'POST':
        form = ComandaForm(request.POST)
        
        pedidoJSON = request.POST.get('pedido') 
        if pedidoJSON:
            pedidoDicc = json.loads(pedidoJSON) # Diccionario con la orden convertida desde el JSON
        else:
            form = ComandaForm()
        
        total = 0.0 # Acumulador del total de la orden

        if form.is_valid():
            comandaForm = form.save(commit=False)

            for pedido in pedidoDicc:
                total += (float(pedido['precio']) * int(pedido['cantidad']))
           
            comandaForm.total = total
            comandaForm.save()
            comandaId = comandaForm.id

            # Guardar el contenido inicial de la orden
            ordenForm = OrdenForm() # Orden que pertenece a la comanda
            orden = ordenForm.save(commit=False) # Orden que pertenece a la comanda
            orden.comanda_id = comandaId
            orden.save()
            ordenId = orden.id # ID de la orden recien creada

            for p in pedidoDicc:
                contenido = OrdenMenu()
                contenido.idOrden = ordenId
                contenido.idMenu = int(p['id'])
                contenido.cantidad = int(p['cantidad'])
                contenido.nota = p['nota']
                contenido.save()

                if(p['tipo'] == 'c'): # hay algo de cocinaen el pedido?
                    orden.cocina = 1

                if(p['tipo'] == 'b'): # Hay algo de bevida en el pedido
                    orden.bebida = 1
                    
            orden.save()

            return redirect('orden_lista')
        else:
            form = ComandaForm()
    else:
        form = ComandaForm()
 
    return render(request, 'comanda/crear.html', {'form':form})

def DetalleOrdenTemp(request): # DETALLE ------------------------------------------------------------------------
    pk = request.GET.get('id') # que viene del AJAX
    comanda = get_object_or_404(Comanda, id = pk)  
    ordenes = Orden.objects.filter(comanda_id = comanda.id).order_by('id')
    
    contenidos = []
    for orden in ordenes:
        res = getOrderDetail(orden.id, 'all') #Obtener detalle de la orden por su ID, y por tipo de procuto (comida[c], bebida[b], todos[all].)
        for r in res:
            contenidos.append(r)

    return render(request, 'comanda/detalle.html', {'comanda': comanda, 'ordenes': ordenes, 'contenidos': contenidos})

def AgregarContenido(request, pk): # AGREGAR COSAS AL PEDIDO -------------------------------------------------------
    comanda = get_object_or_404(Comanda, id = pk)  
    ordenes = Orden.objects.filter(comanda_id = comanda.id).order_by('id')

    contenidos = []
    for orden in ordenes:
        res = getOrderDetail(orden.id, 'all') #Obtener detalle de la orden por su ID, y por tipo de procuto (comida[c], bebida[b], todos[all].)
        for r in res:
            contenidos.append(r)

    if request.method == 'POST':
        total = 0.0

        pedidoJSON = request.POST.get('pedido') 
        if pedidoJSON:
            pedidoDicc = json.loads(pedidoJSON) # Diccionario con la orden convertida desde el JSON
        else:
            return render(request, 'comanda/agregar.html', {'comanda': comanda, 'ordenes': ordenes, 'contenidos': contenidos})

        for pedido in pedidoDicc:
                total += (float(pedido['precio']) * int(pedido['cantidad']))

        # Guardar el contenido nuevo de la orden
        ordenForm = OrdenForm() # Orden que pertenece a la comanda
        orden = ordenForm.save(commit=False) # Orden que pertenece a la comanda
        orden.comanda_id = comanda.id
        orden.agregado = True # Fue añadida despues de la comanda inicial
        orden.save()
        ordenId = orden.id # ID de la orden recien creada
        
        for p in pedidoDicc:
            contenido = OrdenMenu()
            contenido.idOrden = ordenId
            contenido.idMenu = int(p['id'])
            contenido.cantidad = int(p['cantidad'])
            contenido.nota = p['nota']
            contenido.save()

            if(p['tipo'] == 'c'): # hay algo de cocinaen el pedido?
                    orden.cocina = 1

            if(p['tipo'] == 'b'): # Hay algo de bevida en el pedido
                orden.bebida = 1
        
        orden.save()

        comanda.total = comanda.total + decimal.Decimal(total) # Actualizar el total de la orden
        comanda.cobrable = False # se le agregó algo y no se ha entregado,no se puede cobrar
        comanda.save()
        return redirect('orden_lista')

    return render(request, 'comanda/agregar.html', {'comanda': comanda, 'ordenes': ordenes, 'contenidos': contenidos})

def PreguntarBorrarOrden(request): # PARA EL MODAL DE ELIMINAR ----------------------------------------------------
    pk = request.GET.get('id') # que viene del AJAX
    comanda = get_object_or_404(Comanda, id = pk)

    return render(request, 'comanda/borrar.html', {'comanda': comanda})
    
def BorrarOrdenTemp(request, pk): # ELIMINAR ----------------------------------------------------------------------
    comanda = get_object_or_404(Comanda, id = pk) # Primero hallar la comanda, que solo es una
    ordenes = Orden.objects.filter(comanda_id = pk) # Hallar las ordenes de dicha comanda, que pueden ser varias
    
    for orden in ordenes:
        OrdenMenu.objects.filter(idOrden = orden.id).delete() # borrar los contenidos por cada orden de la comanda
    Orden.objects.filter(comanda_id = pk).delete() # Borramos todas la ordenes de la comanda
    comanda.delete() # por último , la comanda

    return redirect('orden_lista')

# Obtener el contenido de una orden temporal específica===========================================================
def getOrderDetail(id, tipo): 
    ordenMenu = OrdenMenu.objects.filter(idOrden = id) # ID's de los contenidos de la orden

    menu = Menu.objects.none()
    content = []
    for om in ordenMenu:
   
        if tipo == 'all':
            menu = Menu.objects.filter(id = om.idMenu).first()
        else:
            menu = Menu.objects.filter(id = om.idMenu).filter(tipo = tipo).first()
        
        if menu: # si hay resultados
            item = {
                'id':menu.id,
                'tipo':menu.tipo, 
                'nombre':menu.nombre, 
                'precio': menu.precio, 
                'cantidad': om.cantidad, 
                'nota': om.nota,
                'idOrden':id
            }
            content.append(item)

    return (content)


# ORDENES PERMANENTES (HISTÓRICO) ===================================================================================================
#====================================================================================================================================

# PENDIENTEEEEEE XD 



# VISTAS PAR LA COCINA  =============================================================================================================
#====================================================================================================================================

def ListadoCocina(request): # LISATDO PARA LA COCINA ------------------------------------------------------------------
    ordenesPend = Orden.objects.filter(Q(cocina = 1) | Q(cocina = 2)).order_by('id') # las que no se han procesado y tienen parte de caomida en ellas
    cantPend = Orden.objects.filter(cocina = 1).count() 
    
    comandas = Comanda.objects.filter(cobrable = False).order_by('id') # Sólo las las "NO cobrables" pués estan pendientes de entregarles algo
    contenidos = [] # de cada orden
    
    for orden in ordenesPend:
        print(orden.id)
        content = getOrderDetail(orden.id, 'c')
        if content: #  si hay resultados
            for c in content:
                contenidos.append(c)

    return render(request,'cocina/lista.html', {'comandas': comandas, 'ordenes' : ordenesPend,'cantPend': cantPend, 'contenidos':contenidos})


def CambiarEstadoCocina(request, pk): # FINALIZAR PEDIDO COCINA ------------------------------------------------------------
    orden = get_object_or_404(Orden, id = pk)
    orden.cocina = 2 # cocina hecha 
    orden.save()

    return redirect('cocina_lista')


# VISTAS PAR LA COCINA  =============================================================================================================
#====================================================================================================================================

def ListadoBebida(request): # LISATDO PARA LA COCINA ------------------------------------------------------------------
    ordenesPend = Orden.objects.filter(Q(bebida = 1) | Q(bebida = 2)).order_by('id') # las que tiene parte de bebida en su orden
    cantPend = Orden.objects.filter(bebida = 1).count() 

    comandas = Comanda.objects.filter(cobrable = False).order_by('id') # Sólo las las "NO cobrables" pués estan pendientes de entregarles algo
    contenidos = []

    for orden in ordenesPend:
        content = getOrderDetail(orden.id, 'b')
        if content: #  si hay resultados
            for c in content:
                contenidos.append(c)

    return render(request,'bebida/lista.html', {'comandas': comandas, 'ordenes' : ordenesPend,'cantPend': cantPend, 'contenidos':contenidos})


def CambiarEstadoBebida(request, pk): # FINALIZAR PEDIDO COCINA ------------------------------------------------------------
    orden = get_object_or_404(Orden, id = pk)
    orden.bebida = 2 # cocina hecha 
    orden.save()

    return redirect('bebida_lista')


# VISTAS PAR LOS MESEROS ============================================================================================================
#====================================================================================================================================

def ListadoMesero(request): # LISATDO DE ORDENES LISTAS PARA ENTREGAR --------------------------------------------------------
    ordenesFin = Orden.objects.filter(Q(cocina = 2) | Q(bebida = 2)).order_by('id') # las de "nuevo=True" son las que no se han procesado
    cocinaPend = Orden.objects.filter(cocina = 2).count() 
    bebidaPend = Orden.objects.filter(bebida = 2).count()
     
    comandas = Comanda.objects.filter(cobrable = False).order_by('id') # Sólo las las "NO cobrables" pués estan pendientes de entregarles algo
    contenidos = []

    for orden in ordenesFin:
        content = getOrderDetail(orden.id, 'all')
        if content: #  si hay resultados
            for c in content:
                contenidos.append(c)

    return render(request,'mesero/lista.html', {'comandas': comandas, 'ordenes': ordenesFin, 'contenidos': contenidos, 'cantComidas': cocinaPend, 'cantBebidas': bebidaPend})

def EntregarComida(request, pk): # FINALIZAR PEDIDO ENTREGADO EN MESA ---------------------------------------------------
    orden = get_object_or_404(Orden, id = pk)
    orden.cocina = 3 # comida hecha y entregada a la mesa
    orden.save()

    estadoComanda(orden.comanda_id)

    orden.save()
    return redirect('entregas_lista')

def EntregarBebida(request, pk): # FINALIZAR PEDIDO ENTREGADO EN MESA ---------------------------------------------------
    orden = get_object_or_404(Orden, id = pk)
    orden.bebida = 3 # comida hecha y entregada a la mesa
    orden.save()

    estadoComanda(orden.comanda_id)

    orden.save()
    return redirect('entregas_lista')

def estadoComanda (comandaId): # SI LA COMANDA SE PUEDE COBRAR ----------------------------------------------------------
    comanda = get_object_or_404(Comanda, id = comandaId) # comanda de la orden por finalizar
    pendientes = Orden.objects.filter(Q(comanda_id = comanda.id) & (Q(cocina = 2) | Q(bebida = 2))).count()
    print(pendientes)
    if pendientes == 0:
        print('no hay pendientes')
        comanda.cobrable = True
        comanda.save()