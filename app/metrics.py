from saidas.models import Saidas
from entradas.models import Entradas
from bitcoin.models import TransacaoBTC

from django.db.models import Sum, Q


def obter_metricas_dashboard():
    total_saidas = Saidas.objects.aggregate(valor_total=Sum('valor'))
    total_entradas = Entradas.objects.aggregate(valor_total=Sum('valor'))

    total_gasto_btc = TransacaoBTC.objects.aggregate(
        total_gasto_btc=Sum(
            'valor_total', 
            filter=Q(tipo='compra_recorrente') | Q(tipo='compra')
        )
    )

    total_liquido_btc = TransacaoBTC.objects.aggregate(
        total_liquido_btc=Sum(
            'valor_liquido', 
            filter=Q(tipo='compra_recorrente') | Q(tipo='compra')
        )
    )

    envio_btc_total = TransacaoBTC.objects.aggregate(
        envio_btc_total=Sum(
            'valor_total', 
            filter=Q(tipo='envio_onchain')
        )
    )

    envio_btc_liquido = TransacaoBTC.objects.aggregate(
        envio_btc_liquido=Sum(
            'valor_liquido', 
            filter=Q(tipo='envio_onchain')
        )
    )

    total_satoshis_comprados = TransacaoBTC.objects.aggregate(
        total_satoshis_comprados=Sum(
            'satoshis', 
            filter=Q(tipo='compra_recorrente') | Q(tipo='compra')
        )
    )

    total_satoshis_enviados = TransacaoBTC.objects.aggregate(
        total_satoshis_enviados=Sum(
            'satoshis', 
            filter=Q(tipo='envio_onchain')
        )
    )

    print("========== Saidas ==========")
    print(f"Saidas: {total_saidas}")
    print("========== Entradas ==========")
    print(f"Entradas: {total_entradas}")
    print("========== BTC ==========")
    print(f"Gasto BTC: {total_gasto_btc}")
    print(f"Gasto Liquido BTC: {total_liquido_btc}")
    print(f"Envio BTC: {envio_btc_total}")
    print(f"Envio Liquido BTC: {envio_btc_liquido}")
    print("========== Satoshis ==========")
    print(f"Satoshis Comprados: {total_satoshis_comprados}")
    print(f"Satoshis Enviados: {total_satoshis_enviados}")

    return dict(
        total_saidas = total_saidas,
        total_entradas = total_entradas,

        total_gasto_btc = total_gasto_btc,
        total_liquido_btc = total_liquido_btc,
        
        envio_btc_total = envio_btc_total,
        envio_btc_liquido = envio_btc_liquido,
        
        total_satoshis_comprados = total_satoshis_comprados,
        total_satoshis_enviados = total_satoshis_enviados
    )