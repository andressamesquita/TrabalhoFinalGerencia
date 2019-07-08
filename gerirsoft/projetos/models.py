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
    hora_prazo = models.TimeField()
    dono = models.ForeignKey("perfis.Gestor", on_delete=models.CASCADE, related_name="projetos", null=True)
    statusProjeto = models.CharField(max_length=20, choices=STATUS_CHOICES, null=False, blank=False) 

class Tarefa(models.Model):
    STATUS_CHOICES = (
        ('PENDENTE','pendente'),
        ('EM DESENVOLVIMENTO','em desenvolvimento'),
        ('FEITO','finalizado')
    )

    nome_tarefa = models.CharField(max_length=255, null=False)
    data_prazo = models.DateTimeField(auto_now_add=False)
    hora_prazo = models.TimeField()
    responsavel = models.ForeignKey('perfis.Membro', on_delete=models.CASCADE, related_name="responsavel")
    statusTarefa = models.CharField(max_length=1, choices=STATUS_CHOICES, null=False, blank=False) 
    p = models.ForeignKey('Projeto', on_delete=models.CASCADE, related_name="tarefas", null=True)


class Time(models.Model):
    dono = models.ForeignKey("perfis.Gestor", on_delete=models.CASCADE, related_name="dono", null=True)
    membros = models.ManyToManyField('perfis.Membro', related_name = 'membros_time', symmetrical=False, through='MembrosTime')
    
class MembrosTime(models.Model):
    membro = models.ForeignKey("perfis.Membro", on_delete=models.CASCADE, related_name="membros", null=True)
    time = models.ForeignKey("Time", on_delete=models.CASCADE, related_name="time", null=True)

    
    #Cada gestor terá seu próprio time.
    #Pode haver mais de um usuário com o mesmo email?
    #Um usuário pode estar cadastrado em mais de uma equipe? pq seria o mesmo email...
    #Descobrir como enviar um email pelo django
    #Como gerar o code do usuário... será o id dele?