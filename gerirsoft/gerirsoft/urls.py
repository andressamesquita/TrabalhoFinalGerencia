"""gerirsoft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from perfis.views import *
from django.contrib.auth import views as v

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', abertura, name='abertura'),
    path('index', index, name = 'index'),
    path('projeto/detail/<int:projeto_id>', projetoDetail, name = 'projetoDetail'),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', v.LogoutView.as_view(template_name = 'login.html'), name="logout"),
    path('registrar/', RegistrarUsuarioView.as_view(), name="registrar"),
    path('gestor/time/', verTime, name='meuTime'),
    path('gestor/projetos', verProjetos, name='meusProjetos'),
    path('gestor/projetos/novoProjeto', RegistrarProjetoView.as_view(), name='novoProjeto'),
    path('gestor/projetos/novoMembro', RegistrarMembroView.as_view(), name='novoMembro'),
    path('gestor/projetos/<int:projeto_id>/excluir', deletar_projeto, name='excluir_projeto'),
    path('gestor/time/<int:membro_id>/excluir', deletar_membro, name='excluir_membro'),
    path('projeto/detail/novaTarefa/<int:projeto_id>', RegistrarTarefaView.as_view(), name='novaTarefa'),

]
