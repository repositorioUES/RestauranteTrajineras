from django.urls import path
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve
from .views import *


urlpatterns = [
    # path('administrador', index, name="index"),

    path('administrador/menu-lista', ListadoMenu, name='menu_lista'),
    path('administrador/menu-crear', CrearMenu, name='menu_crear'),
    path('administrador/menu-editar/<int:pk>', EditarMenu, name='menu_editar'),
    path('administrador/menu-borrar/<int:pk>', BorrarMenu, name='menu_borrar'),
    
    path('general/orden-lista', ListadoOrdenTemp, name='orden_lista'),
    path('general/orden-crear', CrearOrdenTemp, name='orden_crear'),
    path('general/orden-editar', ListadoOrdenTemp, name='orden_editar'),
    path('general/orden-borrar', ListadoOrdenTemp, name='orden_borrar'),
    # path('administrador/crearCategoria', CrearCategoria.as_view(), name="crear_categoria"),
    # path('administrador/modificarCategoria/<int:pk>', ModificarCategoria.as_view(), name='modificar_categoria'),
    # path('administrador/borrarCategoria/<id>',borrarCategoria, name='borrar_categoria'),
    
]