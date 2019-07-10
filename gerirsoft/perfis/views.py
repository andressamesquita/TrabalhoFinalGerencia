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
import random
from django.db import transaction
#from django.core.mail import EmailMessage


def abertura(request):
	return render(request, 'gerirSoft.html')

def projetoDetail(request, projeto_id):
	projeto = Projeto.objects.get(id=projeto_id)
	tarefas = Tarefa.objects.filter(projeto=projeto_id)
	contexto = {
		"tarefas": tarefas,
		"projeto": projeto
	}

	return render(request, 'projetoDetail.html', contexto)

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
	
	@transaction.atomic
	def post(self, request):
		form = RegistrarUsuarioForm (request.POST)
		if form.is_valid ():
			dados_form = form.cleaned_data
			usuario = User.objects.create_user (username = dados_form['nome'], email = dados_form['email'], password = dados_form['senha'])
			perfil = Gestor(nome=dados_form['nome'], usuario = usuario)
			perfil.save()
			time = Time(dono = perfil)
			time.save()
			return redirect('index')

		return render(request, self.template_name, {'form':form})

def verTime(request):
	usuario_logado = get_usuario_logado(request)
	
	time = Time.objects.get(dono=usuario_logado.gestor.id)
	membrosTime = MembrosTime.objects.filter(time = time)

	contexto = {
		'perfil_logado': usuario_logado,
		'time':membrosTime
	}

	return render(request, 'meuTime.html', contexto)

@login_required
def deletar_membro(request, membro_id):
	membro = Membro.objects.get(id=membro_id)
	membro.excluir_membro()
	
	usuario_logado = get_usuario_logado(request)
	
	time = Time.objects.get(dono=usuario_logado.gestor.id)
	membrosTime = MembrosTime.objects.filter(time = time)

	contexto = {
		'perfil_logado': usuario_logado,
		'time':membrosTime
	}

	return render(request, 'meuTime.html', contexto)



def verProjetos(request):
	usuario_logado = get_usuario_logado(request)
	projetos = Projeto.objects.filter(dono=usuario_logado.gestor.id)

	contexto = {
		'perfil_logado': usuario_logado,
		'projetos':projetos
	}

	return render(request, 'meusProjetos.html', contexto)


@login_required
def deletar_projeto(request, projeto_id):
	projeto = Projeto.objects.get(id=projeto_id)
	projeto.excluir_projeto()
	
	usuario_logado = get_usuario_logado(request)
	projetos = Projeto.objects.filter(dono=usuario_logado.gestor.id)

	contexto = {
		'perfil_logado': usuario_logado,
		'projetos':projetos
	}

	return render(request, 'meusProjetos.html', contexto)
	


class RegistrarProjetoView(View):
	template_name = 'registrarProjeto.html'

	def get(self, request):
		return render (request, self.template_name)
	
	def post(self, request):
		form = RegistrarProjetoForm (request.POST)
		if form.is_valid ():
			dados_form = form.cleaned_data
			projeto = Projeto(nome = dados_form['nome'], data_prazo = dados_form['data'], hora_prazo = dados_form['hora'], statusProjeto = dados_form['status'], dono = get_usuario_logado(request).gestor)
			projeto.save()
			
			usuario_logado = get_usuario_logado(request)
			projetos = Projeto.objects.filter(dono=usuario_logado.gestor.id)

			contexto = {
				'perfil_logado': usuario_logado,
				'projetos':projetos
			}

			return render(request, 'meusProjetos.html', contexto)

		return render(request, self.template_name, {'form':form})

class RegistrarMembroView(View):
	template_name = 'registrarMembro.html'

	def get(self, request):
		return render (request, self.template_name)
	
	def post(self, request):
		form = RegistrarMembroForm (request.POST)
		if form.is_valid ():
			dados_form = form.cleaned_data
			senha = gerarSenha()
			usuario = User.objects.create_user (username = dados_form['nome'], email = dados_form['email'], password = senha)
			membro = Membro(nome = dados_form['nome'], funcao = dados_form['funcao'], usuario = usuario, code = senha)
			membro.save()
			time = getTime(request)
			relacionarMembroTime(membro, time)

			usuario_logado = get_usuario_logado(request)
	
			time = Time.objects.get(dono=usuario_logado.gestor.id)
			membrosTime = MembrosTime.objects.filter(time = time)

			contexto = {
				'perfil_logado': usuario_logado,
				'time': membrosTime
			}

			return render(request, 'meuTime.html', contexto)

		return render(request, self.template_name, {'form':form})


def gerarSenha():
	senha = ""
	alfa = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z" ]
	index = random.randint(0,25)
	senha += alfa[index]
	numero = random.randint(0,199)
	senha += str(numero)
	index = random.randint(0,25)
	senha += alfa[index]
	numero = random.randint(0,199)
	senha += str(numero)

	return senha

def relacionarMembroTime(membro, time):
	membrosTime = MembrosTime()
	membrosTime.membro = membro
	membrosTime.time = time
	membrosTime.save()

def getTime(request):
	usuario_logado = Gestor.objects.get(id=get_usuario_logado(request).gestor.id)
	time = Time.objects.get(dono=usuario_logado)
	return time
	

class RegistrarTarefaView(View):
	template_name = 'registrarTarefa.html'

	def get(self, request, projeto_id):
		projeto = Projeto.objects.get(id=projeto_id)

		contexto = {
			"projeto": projeto
		}

		return render (request, self.template_name, contexto)
	
	def post(self, request, projeto_id):
		form = RegistrarTarefaForm (request.POST)
		if form.is_valid ():
			dados_form = form.cleaned_data
			projeto = Projeto.objects.get(id=projeto_id)
			tarefa = Tarefa(nome_tarefa = dados_form['nome'], data_prazo = dados_form['data'], hora_prazo = dados_form['hora'], statusTarefa = dados_form['status'], projeto = projeto)
			tarefa.save()
			
			projeto = Projeto.objects.get(id=projeto_id)
			tarefas = Tarefa.objects.filter(projeto=projeto_id)
			contexto = {
				"tarefas": tarefas,
				"projeto": projeto
			}

			return render(request, 'projetoDetail.html', contexto)


		return render(request, self.template_name, {'form':form})


def adicionar_membro_tarefa(request, tarefa_id):
	tarefa = Tarefa.objects.get(id = tarefa_id)
	time = Time.objects.get(dono = get_usuario_logado(request).gestor.id)
	membrosTime = MembrosTime.objects.filter(time=time)

	contexto = {
		'tarefa':tarefa,
		'time':membrosTime
	}

	return render(request, 'adicionaMembro.html', contexto)

def membro_tarefa(request, tarefa_id, membro_id):
	tarefa = Tarefa.objects.get(id = tarefa_id)
	perfil = Membro.objects.get(id = membro_id)
	tarefa.responsavel = perfil
	tarefa.save()
	
	return redirect('index')


def minhaTimeLine(request):
	membro = Membro.objects.get(id = get_usuario_logado(request).membro.id)
	tarefas = membro.get_minhas_tarefas()
	print(tarefas)
	contexto = {
		'tarefas':tarefas
	}
	return render(request, 'minhaTimeLine.html', contexto)

def projetosMembro(request):
	membro = Membro.objects.get(id = get_usuario_logado(request).membro.id)
	projetos = membro.get_meus_projetos()
	contexto = {
		'projetos':projetos
	}
	return render(request, 'projetosMembro.html', contexto)