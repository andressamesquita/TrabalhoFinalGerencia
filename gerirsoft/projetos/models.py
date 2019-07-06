from django.db import models
from perfis.models import *

# Create your models here.

class Projeto(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE','pendente'),
        ('EM DESENVOLVIMENTO','em desenvolvimento'),
        ('FEITO','finalizado')
    )
    
    nome = models.CharField(max_length=255, null=False)
    data_prazo = models.DateTimeField(auto_now_add=False)
    hr_prazo = models.TimeField()

    tarefas = models.ForeignKey(Tarefa, on_delete=models.CASCADE, related_name="tarefas")
    statusProjeto = models.CharField(max_length=1, choices=STATUS_CHOICES, null=False, blank=False) 

class Tarefa(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE','pendente'),
        ('EM DESENVOLVIMENTO','em desenvolvimento'),
        ('FEITO','finalizado')
    )

    nome_tarefa = models.CharField(max_length=255, null=False)
    data_prazo = models.DateTimeField(auto_now_add=False)
    hr_prazo = models.TimeField()
    responsavel = models.ForeignKey(Membro, on_delete=models.CASCADE, related_name="responsavel")
    statusTarefa = models.CharField(max_length=1, choices=STATUS_CHOICES, null=False, blank=False) 

class Time(models.Model):
    
    membros = models.ManyToManyField('self', related_name = 'membros_time', symmetrical=False, through='Membro')
    

    
    #Cada gestor terá seu próprio time.
    #Pode haver mais de um usuário com o mesmo email?
    #Um usuário pode estar cadastrado em mais de uma equipe? pq seria o mesmo email...
    #Descobrir como enviar um email pelo django
    #Como gerar o code do usuário... será o id dele?