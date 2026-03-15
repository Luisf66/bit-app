from django.db import models


# Categoria da transação
class Categoria(models.Model):

    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

# Model Base para Ganho e Gasto
class TransacaoBase(models.Model):

    descricao = models.CharField(max_length=200)

    valor = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    data = models.DateTimeField()

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        abstract = True

# Model para Ganho
class Ganho(TransacaoBase):

    def __str__(self):
        return f"Ganho - {self.descricao}"
    
# Model para Gasto
class Gasto(TransacaoBase):

    def __str__(self):
        return f"Gasto - {self.descricao}"

# Model para Importação de CSV cripto (BIPA)
class ImportacaoCSV(models.Model):

    arquivo = models.FileField(upload_to="csv_imports/")

    criado_em = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"CSV {self.id}"