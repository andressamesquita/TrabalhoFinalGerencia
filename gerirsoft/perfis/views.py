from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db import transaction
from django.contrib.auth.decorators import login_required
from perfis.forms import *
from perfis.models import *

@login_required
def index(request):

    contexto = {
        'perfil_logado': get_usuario_logado(request)
    }
    
    return render(request, 'index.html', contexto)

@login_required
def get_usuario_logado(request):	
	return request.user

class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            login(request, user)
            return redirect('index')

        return render(request, self.template_name, {"form":form})

class RegistrarUsuarioView(View):
	template_name = 'registrar.html'

	def get(self, request):
		return render (request, self.template_name)
	
	def post(self, request):
		form = RegistrarUsuarioForm (request.POST)
		if form.is_valid ():
			dados_form = form.cleaned_data
			usuario = User.objects.create_user (username = dados_form['nome'], email = dados_form['email'], password = dados_form['senha'])
			perfil = Gestor(nome=dados_form['nome'], usuario = usuario)
			perfil.save()
			return redirect('index')

		return render(request, self.template_name, {'form':form})


