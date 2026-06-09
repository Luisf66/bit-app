import factory
import uuid
from django.utils import timezone
from decimal import Decimal
from bitcoin.models import TransacaoBTC
from usuarios.test.factory.factory import UsuarioFactory


class TransacaoBTCFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TransacaoBTC

    usuario = factory.SubFactory(UsuarioFactory)
    hash = factory.LazyFunction(lambda: uuid.uuid4().hex)  # ← 32 chars exatos
    ativo = 'BTC'
    movimentacao = 'entrada'
    tipo = 'compra'
    valor_total = Decimal('500.00')
    valor_liquido = Decimal('490.00')
    satoshis = Decimal('0.00100000')
    taxa_porcentual = Decimal('2.00')
    taxa_ativo = 'BRL'
    taxa_quantidade = Decimal('10.00')
    cotacao_do_dia = Decimal('500000.00')
    origem = 'pix'
    destino = 'carteira'
    data = factory.LazyFunction(timezone.now)  # ← com timezone