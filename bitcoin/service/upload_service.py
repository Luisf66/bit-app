import hashlib
import pandas as pd
from decimal import Decimal, InvalidOperation
from django.db import transaction, IntegrityError
from bitcoin.models import TransacaoBTC


COLUNAS_ESPERADAS = [
    'Ativo', 'Movimentacao', 'Tipo', 'ValorTotal', 'ValorLiquido',
    'Satoshis', 'TaxaPorcentual', 'TaxaAtivo', 'TaxaQuantidade',
    'CotacaoDia', 'Origem', 'Destino', 'Data'
]

# índices posicionais usados na leitura (contrato com o CSV)
IDX_ATIVO          = 0
IDX_MOVIMENTACAO   = 1
IDX_TIPO           = 2
IDX_VALOR_TOTAL    = 3
IDX_VALOR_LIQUIDO  = 4
IDX_SATOSHIS       = 5
IDX_TAXA_PERCENT   = 6
IDX_TAXA_ATIVO     = 7
IDX_TAXA_QTDE      = 8
IDX_COTACAO        = 9
IDX_ORIGEM         = 10
IDX_DESTINO        = 11
IDX_DATA           = 12


class CSVInvalidoError(Exception):
    """Arquivo CSV não atende ao formato esperado."""


class BitcoinUploadService:

    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.df = None
        self.transacoes_salvas = 0
        self.transacoes_ignoradas = 0

    # ------------------------------------------------------------------ #
    #  Público                                                             #
    # ------------------------------------------------------------------ #

    def validate_csv(self) -> None:
        """
        Lê o arquivo, valida número de colunas, parse de datas e
        tipos decimais. Levanta CSVInvalidoError com mensagem clara.
        """
        try:
            self.df = pd.read_csv(self.arquivo, sep=',')
        except Exception as e:
            raise CSVInvalidoError(f"Não foi possível ler o arquivo CSV: {e}")

        # valida número mínimo de colunas
        if self.df.shape[1] < len(COLUNAS_ESPERADAS):
            raise CSVInvalidoError(
                f"O CSV deve ter pelo menos {len(COLUNAS_ESPERADAS)} colunas, "
                f"mas tem {self.df.shape[1]}."
            )

        # valida parse de datas
        try:
            self.df['Data'] = pd.to_datetime(
                self.df.iloc[:, IDX_DATA], format='%d/%m/%Y %H:%M:%S'
            )
            self.df['Data'] = self.df['Data'].dt.tz_localize('America/Sao_Paulo')
        except Exception:
            raise CSVInvalidoError(
                "A coluna 'Data' (posição 12) contém valores fora do "
                "formato esperado: DD/MM/YYYY HH:MM:SS."
            )

        # valida se campos decimais são conversíveis (checa primeira linha)
        indices_decimais = [
            IDX_VALOR_TOTAL, IDX_VALOR_LIQUIDO, IDX_SATOSHIS,
            IDX_TAXA_PERCENT, IDX_TAXA_QTDE, IDX_COTACAO,
        ]
        for idx in indices_decimais:
            try:
                Decimal(str(self.df.iloc[0, idx]))
            except InvalidOperation:
                raise CSVInvalidoError(
                    f"Valor inválido na coluna {idx} — era esperado um número decimal."
                )

    def process_file(self) -> dict:
        """
        Orquestra a importação completa.
        Retorna um dict com o resultado da operação.
        """
        try:
            with transaction.atomic():
                for linha in range(len(self.df)):
                    dados = self._parse_row(linha)
                    self._save_row(dados)
        except Exception as e:
            # rollback do bloco externo já ocorreu
            raise RuntimeError(f"Erro geral durante a importação: {e}") from e

        return {
            'transacoes_salvas': self.transacoes_salvas,
            'transacoes_ignoradas': self.transacoes_ignoradas,
        }

    # ------------------------------------------------------------------ #
    #  Privados                                                            #
    # ------------------------------------------------------------------ #

    def _parse_row(self, linha: int) -> dict:
        """Extrai e converte os campos de uma linha do DataFrame."""
        row = self.df.iloc[linha]

        ativo        = str(row.iloc[IDX_ATIVO]).strip().upper()
        movimentacao = str(row.iloc[IDX_MOVIMENTACAO]).strip().lower()
        tipo         = str(row.iloc[IDX_TIPO]).strip().lower()
        origem       = str(row.iloc[IDX_ORIGEM]).strip().lower()
        destino      = str(row.iloc[IDX_DESTINO]).strip().lower()
        valor_total  = Decimal(str(row.iloc[IDX_VALOR_TOTAL]))
        valor_liq    = Decimal(str(row.iloc[IDX_VALOR_LIQUIDO]))
        satoshis     = Decimal(str(row.iloc[IDX_SATOSHIS]))
        taxa_pct     = Decimal(str(row.iloc[IDX_TAXA_PERCENT]))
        taxa_ativo   = str(row.iloc[IDX_TAXA_ATIVO]).strip().upper()
        taxa_qtde    = Decimal(str(row.iloc[IDX_TAXA_QTDE]))
        cotacao      = Decimal(str(row.iloc[IDX_COTACAO]))
        data         = row['Data']

        return {
            'ativo': ativo, 'movimentacao': movimentacao, 'tipo': tipo,
            'origem': origem, 'destino': destino, 'valor_total': valor_total,
            'valor_liquido': valor_liq, 'satoshis': satoshis,
            'taxa_porcentual': taxa_pct, 'taxa_ativo': taxa_ativo,
            'taxa_quantidade': taxa_qtde, 'cotacao_do_dia': cotacao,
            'data': data,
            'hash': self._generate_hash(
                ativo, movimentacao, tipo, valor_total, valor_liq,
                satoshis, taxa_pct, taxa_ativo, taxa_qtde,
                cotacao, origem, destino, data,
            ),
        }

    def _generate_hash(self, ativo, movimentacao, tipo, valor_total,
                        valor_liquido, satoshis, taxa_porcentual, taxa_ativo,
                        taxa_quantidade, cotacao_do_dia, origem, destino,
                        data) -> str:
        """Gera o hash MD5 identificador único da transação."""
        data_str = data.strftime('%d/%m/%Y %H:%M:%S')
        conteudo = (
            f"{ativo}{movimentacao}{tipo}"
            f"{valor_total}{valor_liquido}{satoshis}"
            f"{taxa_porcentual}{taxa_ativo}{taxa_quantidade}"
            f"{cotacao_do_dia}{origem}{destino}{data_str}"
        )
        return hashlib.md5(conteudo.encode('utf-8')).hexdigest()

    def _save_row(self, dados: dict) -> None:
        """
        Tenta salvar uma transação. Ignora silenciosamente duplicatas
        via savepoint — não interrompe o lote inteiro.
        """
        transacao = TransacaoBTC(**dados)
        try:
            with transaction.atomic():   # savepoint por linha
                transacao.save()
                self.transacoes_salvas += 1
        except IntegrityError:
            self.transacoes_ignoradas += 1