import pytest
from unittest.mock import patch, MagicMock
from usuarios.test.factory.factory import UsuarioFactory
from entradas.test.factory.factory import EntradaFactory, CategoriaEntradaFactory
from saidas.test.factory.factory import SaidaFactory , CategoriaSaidaFactory
from bitcoin.test.factory.factory import TransacaoBTCFactory
from bitcoin.service.dashboard_service import DashboardService


@pytest.mark.django_db
class TestDashboardServiceFinanceiro:

    def test_saldo_correto(self):
        usuario = UsuarioFactory()
        cat_entrada = CategoriaEntradaFactory(usuario=usuario)
        cat_saida = CategoriaSaidaFactory(usuario=usuario)
        EntradaFactory(usuario=usuario, categoria=cat_entrada, valor=1000.00)
        SaidaFactory(usuario=usuario, categoria=cat_saida, valor=300.00)

        with patch('bitcoin.service.dashboard_service.BlockchainService') as mock_bc:
            mock_bc.return_value.get_btc_price.return_value = '300.000,00'
            service = DashboardService(usuario)
            context = service.get_financeiro_context()

        assert context['total_entradas'] == 1000.00
        assert context['total_saidas'] == 300.00
        assert context['saldo'] == 700.00

    def test_saldo_zerado_sem_dados(self):
        usuario = UsuarioFactory()

        with patch('bitcoin.service.dashboard_service.BlockchainService') as mock_bc:
            mock_bc.return_value.get_btc_price.return_value = '300.000,00'
            service = DashboardService(usuario)
            context = service.get_financeiro_context()

        assert context['total_entradas'] == 0
        assert context['total_saidas'] == 0
        assert context['saldo'] == 0

    def test_dados_isolados_por_usuario(self):
        usuario1 = UsuarioFactory()
        usuario2 = UsuarioFactory()
        cat1 = CategoriaEntradaFactory(usuario=usuario1)
        cat2 = CategoriaEntradaFactory(usuario=usuario2)
        EntradaFactory(usuario=usuario1, categoria=cat1, valor=2000.00)
        EntradaFactory(usuario=usuario2, categoria=cat2, valor=5000.00)

        with patch('bitcoin.service.dashboard_service.BlockchainService') as mock_bc:
            mock_bc.return_value.get_btc_price.return_value = '300.000,00'
            service1 = DashboardService(usuario1)
            service2 = DashboardService(usuario2)
            context1 = service1.get_financeiro_context()
            context2 = service2.get_financeiro_context()

        assert context1['total_entradas'] == 2000.00
        assert context2['total_entradas'] == 5000.00


@pytest.mark.django_db
class TestDashboardServiceBTC:

    def test_metricas_btc(self):
        usuario = UsuarioFactory()
        TransacaoBTCFactory(
            usuario=usuario,
            tipo='compra',
            movimentacao='entrada',
            valor_total='1000.00',
            valor_liquido='980.00',
        )

        print(f'Usuario: {usuario}')

        with patch('bitcoin.service.dashboard_service.BlockchainService') as mock_bc:
            mock_bc.return_value.get_btc_price.return_value = '300.000,00'
            service = DashboardService(usuario)
            context = service.get_btc_context()
            print(f'Service: {service}')
            print(f'Context: {context}')

        assert context['total_gasto_btc'] is not None
        assert context['total_liquido_btc'] is not None