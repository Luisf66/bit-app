from django.db import models

# Create your models here.

class Categorias_Saidas(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'Categoria de Saida'
        verbose_name_plural = 'Categorias de Saidas'

    def __str__(self):
        return self.nome

class Saidas(models.Model):
    data = models.DateField()
    valor = models.FloatField()
    descricao = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categorias_Saidas, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Saida'
        verbose_name_plural = 'Saidas'

    def __str__(self):
        return f"{self.valor} - {self.categoria}"