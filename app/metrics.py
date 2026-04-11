from saidas.models import Saidas
from entradas.models import Entradas
from bitcoin.models import TransacaoBTC

from django.db.models import Sum, Q, FloatField
from django.db.models.functions import Cast
from django.utils.formats import number_format


def obter_saldo():
    total_saidas = Saidas.objects.aggregate(
        valor_total_saidas=Sum('valor')
    )['valor_total_saidas'] or 0

    total_entradas = Entradas.objects.aggregate(
        valor_total_entradas=Sum('valor')
    )['valor_total_entradas'] or 0

    saldo = total_entradas - total_saidas

    return {
        'total_saidas': total_saidas,
        'total_entradas': total_entradas,
        'saldo': saldo,
    }


def obter_metricas():

    btc_metrics = TransacaoBTC.objects.aggregate(
        total_gasto_btc=Sum('valor_total', filter=Q(tipo__in=['compra', 'compra_recorrente'])),
        total_liquido_btc=Sum('valor_liquido', filter=Q(tipo__in=['compra', 'compra_recorrente'])),
        envio_btc_total=Sum('valor_total', filter=Q(tipo='envio_onchain')),
        envio_btc_liquido=Sum('valor_liquido', filter=Q(tipo='envio_onchain')),
        total_satoshis_comprados=Sum('satoshis', filter=Q(tipo__in=['compra', 'compra_recorrente'])),
        total_satoshis_enviados=Sum('satoshis', filter=Q(tipo='envio_onchain')),
    )

    taxas_pagas_compra = (btc_metrics['total_gasto_btc'] or 0) - (btc_metrics['total_liquido_btc'] or 0)
    taxas_pagas_envio = (btc_metrics['envio_btc_total'] or 0) - (btc_metrics['envio_btc_liquido'] or 0)

    return {
        'total_gasto_btc': number_format(btc_metrics['total_gasto_btc'] or 0, decimal_pos=2),
        'total_liquido_btc': number_format(btc_metrics['total_liquido_btc'] or 0, decimal_pos=2),
        'taxas_pagas_compra': number_format(taxas_pagas_compra, decimal_pos=2),

        'envio_btc_total': number_format(btc_metrics['envio_btc_total'] or 0, decimal_pos=2),
        'envio_btc_liquido': number_format(btc_metrics['envio_btc_liquido'] or 0, decimal_pos=2),
        'taxas_pagas_envio': number_format(taxas_pagas_envio, decimal_pos=2),

        'total_satoshis_comprados': number_format(btc_metrics['total_satoshis_comprados'] or 0, decimal_pos=9),
        'total_satoshis_enviados': number_format(btc_metrics['total_satoshis_enviados'] or 0, decimal_pos=9),
    }

def obter_dashboard():
    datas, tipos, valores, satoshis, cotacoes = [], [], [], [], []

    btc_dashboard = TransacaoBTC.objects.filter(
        movimentacao='entrada',
        tipo__in=['compra_recorrente', 'compra']
    ).values_list(
        'data',
        'tipo',
        Cast('valor_liquido', FloatField()),
        Cast('satoshis', FloatField()),
        Cast('cotacao_do_dia', FloatField())
    )

    if btc_dashboard.exists():
        datas, tipos, valores, satoshis, cotacoes = (list(col) for col in zip(*btc_dashboard))

    if datas:
        datas = [d.strftime('%d/%m/%Y %H:%M:%S') for d in datas]

    return {
        'datas_transacoes': datas,
        'tipos_transacoes': tipos,
        'valores_transacoes': valores,
        'satoshis_transacoes': satoshis,
        'cotacoes_transacoes': cotacoes
    }
