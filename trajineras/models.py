from django.db import models

# Create your models here.

# Modelo del MENU -------------------------------------------------------------------
class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,help_text="")

    TIPO = (('c','Comida'),('b', 'Bebida'))# Estructura para la selección del tipo de producto
    tipo = models.CharField(max_length=10, choices=TIPO, blank=True, help_text='')

    precio = models.DecimalField(max_digits = 5, decimal_places= 2)

    # El producto esta activo o no
    activo = models.BooleanField(blank=True,  default=1)
    
    def __str__(self): #Para que retorne el nombre y no el Id
        return self.nombre
#FIN MENU
    
# Modelo del ORDEN_TEMP -------------------------------------------------------------------
class OrdenTemp(models.Model):
    id = models.AutoField(primary_key=True)
    mesa = models.IntegerField()
    fechaHora = models.DateTimeField(auto_now_add = True)# fecha y hora de creacion de la orden
    cocina = models.BooleanField(blank=True,  default=0) # esta terminada la parte de cocina de la orden
    bebida = models.BooleanField(blank=True,  default=0) # esta termianda la parte de bebida de la orden
    cobrable = models.BooleanField(blank=True, default=0) # esta lista la orden para ser cobrada
    total = models.DecimalField(max_digits = 10, decimal_places= 2)
    cliente = models.CharField(max_length=150,help_text="")
    
    def __str__(self): #Para que retorne el nombre y no el Id
        return "Mesa:" + str(self.mesa) + " - Fecha:" + str(self.fechaHora)
#FIN ORDEN_TEMP    
    
# Modelo del ORDEN_MENU -------------------------------------------------------------------
class OrdenMenu(models.Model):
    id = models.AutoField(primary_key=True)
    idOrden = models.IntegerField()
    idMenu = models.IntegerField()

    cantidad = models.IntegerField()
    nuevo = models.BooleanField(default=0) # Es un producto agregado despues o es del pedido original?
    
#FIN ORDEN_MENU    