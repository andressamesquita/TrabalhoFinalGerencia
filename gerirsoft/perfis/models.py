from django.db import models
from django.contrib.auth.models import User
from projetos.models import *

# Create your models here.
    
class Gestor(models.Model):
    nome =  models.CharField(max_length=255, null=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gestor')


    @property
    def email(self):
        return self.usuario.email

class Membro(models.Model):
    nome =  models.CharField(max_length=255, null=False)
    funcao = models.CharField(max_length=255, null=False)
    code = models.CharField(max_length=255, null=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membro')


    def get_minhas_tarefas(self):
        tarefas = Tarefa.objects.filter(responsavel = self.id)
        return tarefas


    def get_meus_projetos(self):
        tarefas = self.get_minhas_tarefas()
        projetos = []
        for tarefa in tarefas:
            if tarefa.projeto not in projetos:
                projetos.append(tarefa.projeto)

        return projetos


    @property
    def email(self):
        return self.usuario.email

    def excluir_membro(self):
        self.delete()