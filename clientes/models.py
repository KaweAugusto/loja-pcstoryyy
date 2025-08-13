from django.db import models
from django.contrib.auth.models import User


class Categoria(models.TextChoices):
    PLACA_MAE = 'Placa-mãe', 'Placa-mãe'
    PLACA_VIDEO = 'Placa de vídeo', 'Placa de vídeo'
    PERIFERICO = 'Periférico', 'Periférico'
    OUTROS = 'Outros', 'Outros'


class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField()
    categoria = models.CharField(max_length=20, choices=Categoria.choices)
    imagem = models.URLField(blank=True)

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
