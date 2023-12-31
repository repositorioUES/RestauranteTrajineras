from django.db import models

# Create your models here.

# Modelo del MENU -------------------------------------------------------------------
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,help_text="")
    precio = models.DecimalField(max_digits = 5, decimal_places= 2)
    activo = models.BooleanField(blank=True,  default=1) # El producto esta activo o no

    TIPO = (('c','Comida'),('b', 'Bebida'))# Estructura para la selección del tipo de producto
    tipo = models.CharField(max_length=10, choices=TIPO, blank=True)

    def __str__(self): #Para que retorne el nombre y no el Id
        return self.nombre
#FIN MENU
    
# Modelo del COMANDA -------------------------------------------------------------------
class Comanda(models.Model):
    id = models.AutoField(primary_key=True)
    mesa = models.IntegerField()
    fechaHora = models.DateTimeField(auto_now_add = True)# fecha y hora de creacion de la orden
    total = models.DecimalField(max_digits = 10, decimal_places= 2)
    cobrable = models.BooleanField(blank=True, default=0) # esta lista la orden para ser cobrada
    
    def __str__(self): #Para que retorne el nombre y no el Id
        return "Mesa:" + str(self.mesa) + " - Fecha:" + str(self.fechaHora)
#FIN COMANDA 
    
# Modelo del ORDEN_TEMP -------------------------------------------------------------------
class Orden(models.Model):
    id = models.AutoField(primary_key=True)
    comanda = models.ForeignKey('Comanda', on_delete = models.SET_NULL, null=True)

    # Cocina = 0 - no tiene parte que se cocine
    # Cocina = 1 - SI tiene parte de cocina
    # Cocina = 2 - Ya se realizó la parte de coina, lista para entregar
    # Cocina = 3 - Ya se entregó a la mesa la parte ce cocina del pedido    (TODO ESTO APLICA PARA LA BEBIDA)
    
    cocina = models.IntegerField(default=0) # Controlar el estado de la parte de cocina de la orden
    bebida = models.IntegerField(default=0) # Controlar el estado de la parte de bebida de la orden
    agregado = models.BooleanField(default=0) # No formaba parte del pedido original
    nuevo = models.BooleanField(default=1) # es una orden que no ha sido atendida

#FIN ORDEN_TEMP    
    
# Modelo del ORDEN_MENU -------------------------------------------------------------------
class OrdenMenu(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.IntegerField()
    idMenu = models.IntegerField()
    cantidad = models.IntegerField()
    nota = models.CharField(blank=True, max_length=250)
#FIN ORDEN_MENU    