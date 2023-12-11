from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre']

class SucursalForm(forms.ModelForm):
    class Meta:
        model = Sucursal
        fields = [
            'codigo_sunat', 'nombre', 'direccion', 'departamento',
            'provincia', 'distrito', 'telefono', 'correo_electronico', 'pagina_web'
        ]

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
