from django.db import models
from django.conf import settings
# Create your models here.


class Categorias_Entradas(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria de Entrada'
        verbose_name_plural = 'Categorias de Entradas'

    def __str__(self):
        return self.nome

class Entradas(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    data = models.DateField()
    valor = models.FloatField()
    descricao = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categorias_Entradas, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Entrada'
        verbose_name_plural = 'Entradas'

    def __str__(self):
        return f"{self.categoria} - R${self.valor}"