from django.db import models
from django.conf import settings
# Create your models here.


class TransacaoBTC(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    hash = models.CharField(max_length=32, unique=True)
    # Dados da transação
    ativo = models.CharField(max_length=20)
    movimentacao = models.CharField(max_length=20)
    tipo = models.CharField(max_length=50)
    # Dados monetários
    valor_total = models.DecimalField(max_digits=20, decimal_places=8)
    valor_liquido = models.DecimalField(max_digits=20, decimal_places=8)
    satoshis = models.DecimalField(max_digits=20, decimal_places=8)
    # Taxas
    taxa_porcentual = models.DecimalField(max_digits=10, decimal_places=4)
    taxa_ativo = models.CharField(max_length=20)
    taxa_quantidade = models.DecimalField(max_digits=20, decimal_places=8)
    # Cotação
    cotacao_do_dia = models.DecimalField(max_digits=20, decimal_places=2)
    # Origem e destino
    origem = models.CharField(max_length=50)
    destino = models.CharField(max_length=50)
    # Data
    data = models.DateTimeField()

    class Meta:
        ordering = ['-data']

    def __str__(self):
        return f"{self.tipo} - {self.valor_total} - {self.data}"