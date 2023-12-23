from django.urls import path
from trajineras.views import *
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve


urlpatterns = [
    path('', index, name='index'),

    path('administrador/menu-lista', ListadoMenu, name='menu_lista'),
    path('administrador/menu-crear', CrearMenu, name='menu_crear'),
    path('administrador/menu-editar/<int:pk>', EditarMenu, name='menu_editar'),
    path('administrador/menu-borrar/<int:pk>', BorrarMenu, name='menu_borrar'),
    
    path('general/orden-lista', ListadoOrdenTemp, name='orden_lista'),
    path('general/orden-crear', CrearOrdenTemp, name='orden_crear'),
    path('general/orden-agregar/<int:pk>', AgregarContenido, name='orden_agregar'),
    path('general/orden-detalle',DetalleOrdenTemp, name='orden_detalle'),
    path('general/orden-borrar/<int:pk>', BorrarOrdenTemp, name='orden_borrar'),
   
    
]