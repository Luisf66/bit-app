from django.db import models

# Create your models here.

"""
class TransacaoBTC(models.Model):
    ativo          = models.CharField(max_length=10)
    tipo           = models.CharField(max_length=30)  # E/S
    tipo_transacao = models.CharField(max_length=50)
    valor          = models.DecimalField(max_digits=15, decimal_places=8)
    cotacao        = models.DecimalField(max_digits=15, decimal_places=2)
    origem         = models.CharField(max_length=50)
    destino        = models.CharField(max_length=50)
    data           = models.DateTimeField()

    class Meta:
        ordering = ['-data']
"""