import hashlib
import pandas as pd
from decimal import Decimal
from django.db import IntegrityError, transaction
from django.shortcuts import render
from bitcoin.models import TransacaoBTC
from django.views.generic import ListView

from app import metrics
from bitcoin.utils import get_btc_price, get_wallet_info


class TransacaoListView(ListView):
    model = TransacaoBTC
    template_name = 'bitcoin_list.html'
    context_object_name = 'transacoes'

def DashboardView(request):
    carteira = request.GET.get('carteira', '').strip()
    informacoes_carteira = None
    calculo_saldo_btc_brl = 0

    cotacao_dia = get_btc_price()

    saldo = metrics.obter_saldo()
    informacoes_financeiras = metrics.obter_informacoes_financeiras()
    metricas_btc = metrics.obter_metricas()
    dashboard_btc = metrics.obter_dashboard()

    if carteira: # verifica se a carteira foi buscada
        informacoes_carteira = get_wallet_info(carteira) # busca informacoes da carteira
        if informacoes_carteira.get('saldo_btc'): # se for uma carteira valida
            cotacao_dia = float(cotacao_dia.replace('.', '').replace(',', '.')) # converte cotacao para float
            calculo_saldo_btc_brl = round(informacoes_carteira['saldo_btc'] * cotacao_dia, 2) # calcula o saldo da carteira em reais

    context = {
        'carteira_buscada': carteira,
        'informacoes_carteira': informacoes_carteira,
        'saldo_btc_brl': calculo_saldo_btc_brl,
        'cotacao_dia': cotacao_dia,
        'total_saidas': saldo['total_saidas'],
        'total_entradas': saldo['total_entradas'],
        'saldo': saldo['saldo'],
        'data_entrada': informacoes_financeiras['data_entrada'],
        'valor_entrada': informacoes_financeiras['valor_entrada'],
        'categoria_entrada': informacoes_financeiras['categoria_entrada'],
        'data_saida': informacoes_financeiras['data_saida'],
        'valor_saida': informacoes_financeiras['valor_saida'],
        'categoria_saida': informacoes_financeiras['categoria_saida'],
        'total_gasto_btc': metricas_btc['total_gasto_btc'],
        'total_liquido_btc': metricas_btc['total_liquido_btc'],
        'taxas_pagas_compra': metricas_btc['taxas_pagas_compra'],
        'envio_btc_total': metricas_btc['envio_btc_total'],
        'envio_btc_liquido': metricas_btc['envio_btc_liquido'],
        'taxas_pagas_envio': metricas_btc['taxas_pagas_envio'],
        'total_satoshis_comprados': metricas_btc['total_satoshis_comprados'],
        'total_satoshis_enviados': metricas_btc['total_satoshis_enviados'],
        'datas_transacoes': dashboard_btc['datas_transacoes'],
        'tipos_transacoes': dashboard_btc['tipos_transacoes'],
        'valores_transacoes': dashboard_btc['valores_transacoes'],
        'satoshis_transacoes': dashboard_btc['satoshis_transacoes'],
        'cotacoes_transacoes': dashboard_btc['cotacoes_transacoes'],
        'movimentacoes_transacoes': dashboard_btc['movimentacoes_transacoes'],
    }

    return render(request, 'bitcoin_dashboard.html', context)

def Bitcoin_UploadView(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        df = pd.read_csv(arquivo, sep=',')

        # Converter data
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M:%S')
        df['Data'] = df['Data'].dt.tz_localize('America/Sao_Paulo') # fuso

        transacoes_salvas = 0
        transacoes_ignoradas = 0

        try:
            with transaction.atomic():

                for linha in range(len(df)):

                    # Pegando dados com iloc
                    ativo = str(df.iloc[linha, 0]).strip().upper()
                    movimentacao = str(df.iloc[linha, 1]).strip().lower()
                    tipo = str(df.iloc[linha, 2]).strip().lower()
                    origem = str(df.iloc[linha, 10]).strip().lower()
                    destino = str(df.iloc[linha, 11]).strip().lower()

                    # Conversão segura para Decimal
                    valor_total = Decimal(str(df.iloc[linha, 3]))
                    valor_liquido = Decimal(str(df.iloc[linha, 4]))
                    satoshis = Decimal(str(df.iloc[linha, 5]))
                    taxa_porcentual = Decimal(str(df.iloc[linha, 6]))
                    taxa_ativo = str(df.iloc[linha, 7]).strip().upper()
                    taxa_quantidade = Decimal(str(df.iloc[linha, 8]))
                    cotacao_do_dia = Decimal(str(df.iloc[linha, 9]))

                    data = df.iloc[linha, 12]
                    data_str_hash = data.strftime('%d/%m/%Y %H:%M:%S') # fuso

                    # Hash
                    conteudo = (
                        f"{ativo}{movimentacao}{tipo}"
                        f"{valor_total}{valor_liquido}{satoshis}"
                        f"{taxa_porcentual}{taxa_ativo}{taxa_quantidade}"
                        f"{cotacao_do_dia}{origem}{destino}{data_str_hash}" # fuso
                    )

                    hash_linha = hashlib.md5(conteudo.encode('utf-8')).hexdigest()

                    dados_btc = TransacaoBTC(
                        hash=hash_linha,
                        ativo=ativo,
                        movimentacao=movimentacao,
                        tipo=tipo,
                        valor_total=valor_total,
                        valor_liquido=valor_liquido,
                        satoshis=satoshis,
                        taxa_porcentual=taxa_porcentual,
                        taxa_ativo=taxa_ativo,
                        taxa_quantidade=taxa_quantidade,
                        cotacao_do_dia=cotacao_do_dia,
                        origem=origem,
                        destino=destino,
                        data=data,
                    )

                    try:
                        dados_btc.save()
                        transacoes_salvas += 1
                    except IntegrityError:
                        transacoes_ignoradas += 1
                        print(f"[DUPLICADO] Hash: {hash_linha}")

        except Exception as e:
            print(f"[ERRO GERAL - ROLLBACK] {e}")
            return render(request, 'bitcoin_upload.html')

        print(
            f"Importação finalizada: {transacoes_salvas} salvos, {transacoes_ignoradas} ignorados"
        )

        return render(request, 'bitcoin_dashboard.html')

    return render(request, 'bitcoin_upload.html')