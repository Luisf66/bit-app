import hashlib
import pandas as pd
from decimal import Decimal
from django.db import IntegrityError, transaction
from django.shortcuts import render
from bitcoin.models import TransacaoBTC
from django.views.generic import ListView
from app.metrics import obter_metricas_dashboard

class TransacaoListView(ListView):
    model = TransacaoBTC
    template_name = 'bitcoin_list.html'
    context_object_name = 'transacoes'

def DashboardView(request):
    return render(request, 'bitcoin_dashboard.html', context=obter_metricas_dashboard())

def Bitcoin_UploadView(request):
    if request.method == 'POST' and request.FILES.get('arquivo'):
        arquivo = request.FILES['arquivo']
        df = pd.read_csv(arquivo, sep=',')

        # Converter data
        df['Data'] = pd.to_datetime(df['Data'], format='%d/%m/%Y %H:%M:%S')

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

                    # Hash
                    conteudo = (
                        f"{ativo}{movimentacao}{tipo}"
                        f"{valor_total}{valor_liquido}{satoshis}"
                        f"{taxa_porcentual}{taxa_ativo}{taxa_quantidade}"
                        f"{cotacao_do_dia}{origem}{destino}{data}"
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