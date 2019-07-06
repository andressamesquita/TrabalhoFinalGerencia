from django.db import models
from django.contrib.auth.models import User
from projetos.models import Projeto

# Create your models here.
    
class Gestor(models.Model):
    nome =  models.CharField(max_length=255, null=False)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='gestor')
    projetos = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="projetos")


    @property
    def email(self):
        return self.usuario.email

class Membro(models.Model):
    nome =  models.CharField(max_length=255, null=False)
    funcao = models.CharField(max_lentgh=255, null=False)
    code = models.IntegerField()
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membro')

    @property
    def email(self):
        return self.usuario.email