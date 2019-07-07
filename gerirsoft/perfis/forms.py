    
from django import forms
from django.contrib.auth.models import User

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True)

class RegistrarUsuarioForm(forms.Form):
	nome = forms.CharField(required=True)
	email = forms.EmailField(required=True)
	senha = forms.CharField(required=True)


class RegistrarProjetoForm(forms.Form):
	nome = forms.CharField(required=True)
	data = forms.DateTimeField(required=True)
	hora = forms.TimeField(required=True)
	status = forms.CharField(required=True)

class RegistrarMembroForm(forms.Form):
	nome = forms.CharField(required=True)
	email = forms.CharField(required=True)
	funcao = forms.CharField(required=True)