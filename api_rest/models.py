from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    entidade = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    first_login = models.BooleanField(default=True)


class Arquivos(models.Model):
    id_arquivo = models.IntegerField()
    arquivo = models.TextField()
    nome = models.CharField(max_length=100)

# class dados(models.Model):
#     entidade = models.CharField(max_length=100)
#     uf = models.CharField(max_length=2)
#     descricao = models.CharField(max_length=100)
#     justificativa = models.CharField(max_length=100, default='Digite a sua justificativa.', blank=True, null=True) 
#     data_justificativa = models.DateField(null=True, blank=True) # data carga
#     usuario_justificou = models.CharField(max_length=100, default='', blank=True, null=True) # orientações

#     def __str__(self):
#         return self.entidade + ' | ' + self.uf