import itertools
from saidas.models import Saidas
from entradas.models import Entradas
from bitcoin.models import TransacaoBTC

from django.db.models import Sum, Q, FloatField, Avg
from django.db.models.functions import Cast
from django.utils.formats import number_format


def obter_saldo(usuario):
    total_saidas = Saidas.objects.filter(usuario=usuario).aggregate(
        valor_total_saidas=Sum('valor')
    )['valor_total_saidas'] or 0

    total_entradas = Entradas.objects.filter(usuario=usuario).aggregate(
        valor_total_entradas=Sum('valor')
    )['valor_total_entradas'] or 0

    saldo = total_entradas - total_saidas

    return {
        'total_saidas': total_saidas,
        'total_entradas': total_entradas,
        'saldo': saldo,
    }


def obter_informacoes_financeiras(usuario):
    entradas = (
        Entradas.objects
        .filter(usuario=usuario)
        .values('data')
        .annotate(valor=Sum('valor'))
        .order_by('data')
    )

    saidas = (
        Saidas.objects
        .filter(usuario=usuario)
        .values('data')
        .annotate(valor=Sum('valor'))
        .order_by('data')
    )

    data_entrada, valor_entrada = [], []
    data_saida, valor_saida = [], []

    if entradas.exists():
        for entry in entradas:
            data_entrada.append(entry['data'].strftime('%d/%m/%Y'))
            valor_entrada.append(entry['valor'])

    if saidas.exists():
        for entry in saidas:
            data_saida.append(entry['data'].strftime('%d/%m/%Y'))
            valor_saida.append(entry['valor'])

    valor_entrada_acumulada = list(itertools.accumulate(valor_entrada))

    return {
        'data_entrada': data_entrada,
        'valor_entrada': valor_entrada,
        'valor_entrada_acumulada': valor_entrada_acumulada,
        'data_saida': data_saida,
        'valor_saida': valor_saida,
    }


def obter_metricas(usuario):
    btc_metrics = TransacaoBTC.objects.filter(usuario=usuario).aggregate(
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


def obter_dashboard(usuario):
    datas, tipos, valores, satoshis, cotacoes = [], [], [], [], []

    btc_dashboard = TransacaoBTC.objects.filter(
        usuario=usuario,
        movimentacao='entrada',
        tipo__in=['compra_recorrente', 'compra']
    ).values_list(
        'data',
        'tipo',
        Cast('valor_liquido', FloatField()),
        Cast('satoshis', FloatField()),
        Cast('cotacao_do_dia', FloatField())
    )

    movimentacoes = TransacaoBTC.objects.filter(
        usuario=usuario,
        tipo__in=['compra_recorrente', 'compra', 'envio_onchain']
    ).values_list('movimentacao')

    if btc_dashboard.exists():
        datas, tipos, valores, satoshis, cotacoes = (list(col) for col in zip(*btc_dashboard))

    if movimentacoes:
        movimentacoes = [m[0] for m in movimentacoes]

    if datas:
        datas = [d.strftime('%d/%m/%Y %H:%M:%S') for d in datas]

    datas.reverse()
    valores.reverse()

    return {
        'datas_transacoes': datas,
        'tipos_transacoes': tipos,
        'valores_transacoes': valores,
        'satoshis_transacoes': satoshis,
        'cotacoes_transacoes': cotacoes,
        'movimentacoes_transacoes': movimentacoes,
    }


def obter_preco_medio(usuario):
    preco_medio = TransacaoBTC.objects.filter(
        usuario=usuario,
        movimentacao='entrada',
        tipo__in=['compra_recorrente', 'compra']
    ).aggregate(
        valor_liquido_total=Avg('valor_liquido'),
        valor_satoshis_total=Avg('satoshis')
    )

    if preco_medio['valor_liquido_total'] and preco_medio['valor_satoshis_total']:
        preco_medio_total = preco_medio['valor_liquido_total'] / preco_medio['valor_satoshis_total']
        preco_medio_formatado = f'{preco_medio_total:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
        return preco_medio_formatado

    return 0