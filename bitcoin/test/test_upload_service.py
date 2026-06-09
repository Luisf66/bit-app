import pytest
import io
import pandas as pd
from usuarios.test.factory.factory import UsuarioFactory
from bitcoin.service.upload_service import BitcoinUploadService, CSVInvalidoError


def gerar_csv_valido():
    """Gera um CSV válido em memória para testes."""
    dados = {
        'Ativo': ['BTC'],
        'Movimentacao': ['entrada'],
        'Tipo': ['compra'],
        'ValorTotal': ['500.00'],
        'ValorLiquido': ['490.00'],
        'Satoshis': ['0.00100000'],
        'TaxaPorcentual': ['2.00'],
        'TaxaAtivo': ['BRL'],
        'TaxaQuantidade': ['10.00'],
        'CotacaoDia': ['500000.00'],
        'Origem': ['pix'],
        'Destino': ['carteira'],
        'Data': ['01/01/2025 10:00:00'],
    }
    df = pd.DataFrame(dados)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer


def gerar_csv_invalido():
    """Gera um CSV com colunas insuficientes."""
    dados = {'col1': ['a'], 'col2': ['b']}
    df = pd.DataFrame(dados)
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)
    return buffer


@pytest.mark.django_db
class TestBitcoinUploadService:

    def test_csv_valido_passa_validacao(self):
        usuario = UsuarioFactory()
        service = BitcoinUploadService(gerar_csv_valido(), usuario)
        service.validate_csv()  # não deve levantar exceção

    def test_csv_invalido_levanta_erro(self):
        usuario = UsuarioFactory()
        service = BitcoinUploadService(gerar_csv_invalido(), usuario)
        with pytest.raises(CSVInvalidoError):
            service.validate_csv()

    def test_importacao_salva_transacao(self):
        usuario = UsuarioFactory()
        service = BitcoinUploadService(gerar_csv_valido(), usuario)
        service.validate_csv()
        resultado = service.process_file()

        assert resultado['transacoes_salvas'] == 1
        assert resultado['transacoes_ignoradas'] == 0

    def test_importacao_ignora_duplicata(self):
        usuario = UsuarioFactory()

        service1 = BitcoinUploadService(gerar_csv_valido(), usuario)
        service1.validate_csv()
        service1.process_file()

        service2 = BitcoinUploadService(gerar_csv_valido(), usuario)
        service2.validate_csv()
        resultado = service2.process_file()

        assert resultado['transacoes_salvas'] == 0
        assert resultado['transacoes_ignoradas'] == 1

    def test_transacao_associada_ao_usuario(self):
        from bitcoin.models import TransacaoBTC
        usuario = UsuarioFactory()
        service = BitcoinUploadService(gerar_csv_valido(), usuario)
        service.validate_csv()
        service.process_file()

        transacao = TransacaoBTC.objects.get(usuario=usuario)
        assert transacao.usuario == usuario