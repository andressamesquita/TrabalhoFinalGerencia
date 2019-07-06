from django.db import models
from perfis.models import *
from projetos.models import *

# Create your models here.
class timeline(models.Model):
    perfil = models.OneToOneField(Membro, related_name = "minha_timeline", on_delete = models.CASCADE)

    def get_timeline(self):
        lista_tarefas = []
        tarefas_ordenadas = Tarefa.objects.all()

        for i in tarefas_ordenadas:
            if i.responsavel.id == self.membro.id:
                lista_tarefas.append(i)
        
        return lista_tarefas