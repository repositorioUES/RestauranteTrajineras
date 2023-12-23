from django import forms
from django.contrib.admin import widgets
from django.forms import fields
from django.forms.forms import Form
from django.forms.models import ModelMultipleChoiceField
from django.forms.widgets import SelectMultiple
from trajineras.models import *
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class MenuForm(forms.ModelForm):
	class Meta:
		model = Menu
		fields = [
			 'nombre',
			 'tipo',
			 'precio',
			 'activo'
		]
		labels = {
			'nombre': 'Nombre del Producto',
			'tipo':'Tipo',
			'precio':'Precio',
			'activo':'Disponible',
		}

class OrdenTempForm(forms.ModelForm):
	class Meta:
		model = OrdenTemp
		fields = [
			 'mesa',
			 'cliente'
		]
		labels = {
			'mesa': 'Mesa',
			'cliente':'Cliente'
		}	
		widgets = {
			'mesa':forms.NumberInput (attrs={'class':'input-group input-group-outline'}),
			'cliente':forms.TextInput(attrs={'class':'form-contol'}),
		}	

class OrdenMenuForm(forms.ModelForm):
	class Meta:
		model = OrdenMenu
		fields = [
			'idOrden',
			'idMenu',
			'cantidad',
			'nuevo'
		]
		labels = {
			'idOrden': 'Orden',
			'idMenu': 'Menu',
			'cantidad': 'Cantidad',
			'nuevo': 'Nuevo'
		}	
