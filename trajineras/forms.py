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

class ComandaForm(forms.ModelForm):
	class Meta:
		model = Comanda
		fields = [
			 'mesa'
		]
		labels = {
			'mesa': 'Mesa'
		}	
		widgets = {
			'mesa':forms.NumberInput (attrs={'class':'input-group input-group-outline'}),
			# 'notas':forms.Textarea(attrs={'class':'form-contol','rows':'5'}),
		}	

class OrdenForm(forms.ModelForm):
	class Meta:
		model = Orden
		fields = [
			 'comanda',
			 'cocina',
			 'bebida',
			 'agregado',
			 'nuevo'
		]
