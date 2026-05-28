from app import metrics
from bitcoin.utils import get_btc_price, get_wallet_info


class DashboardService:

    def __init__(self):
        self.cotacao_dia = get_btc_price()

    def get_wallet_context(self, carteira: str) -> dict:
        """
        Busca informações da carteira BTC
        """
        preco_medio = metrics.obter_preco_medio()
        carteira = carteira.strip()
        informacoes_carteira = None
        saldo_btc_brl = 0

        if carteira:
            informacoes_carteira = get_wallet_info(carteira)

            if informacoes_carteira and informacoes_carteira.get('saldo_btc'):
                cotacao_float = float(
                    self.cotacao_dia.replace('.', '').replace(',', '.')
                )
                saldo_btc_brl = round(
                    informacoes_carteira['saldo_btc'] * cotacao_float, 2
                )

        return {
            'preco_medio': preco_medio,
            'carteira_buscada': carteira,
            'informacoes_carteira': informacoes_carteira,
            'saldo_btc_brl': saldo_btc_brl,
        }

    def get_financeiro_context(self) -> dict:
        """
        Dados de Entradas e Saídas informadas pelo usuário
        """
        saldo = metrics.obter_saldo()
        info = metrics.obter_informacoes_financeiras()

        return {
            'total_saidas': saldo['total_saidas'],
            'total_entradas': saldo['total_entradas'],
            'saldo': saldo['saldo'],
            'data_entrada': info['data_entrada'],
            'valor_entrada': info['valor_entrada'],
            'categoria_entrada': info['categoria_entrada'],
            'data_saida': info['data_saida'],
            'valor_saida': info['valor_saida'],
            'categoria_saida': info['categoria_saida'],
        }

    def get_btc_context(self) -> dict:
        """
        Dados das transações da BIPA
        """
        metricas = metrics.obter_metricas()
        dashboard = metrics.obter_dashboard()

        return {
            'total_gasto_btc': metricas['total_gasto_btc'],
            'total_liquido_btc': metricas['total_liquido_btc'],
            'taxas_pagas_compra': metricas['taxas_pagas_compra'],
            'envio_btc_total': metricas['envio_btc_total'],
            'envio_btc_liquido': metricas['envio_btc_liquido'],
            'taxas_pagas_envio': metricas['taxas_pagas_envio'],
            'total_satoshis_comprados': metricas['total_satoshis_comprados'],
            'total_satoshis_enviados': metricas['total_satoshis_enviados'],
            'datas_transacoes': dashboard['datas_transacoes'],
            'tipos_transacoes': dashboard['tipos_transacoes'],
            'valores_transacoes': dashboard['valores_transacoes'],
            'satoshis_transacoes': dashboard['satoshis_transacoes'],
            'cotacoes_transacoes': dashboard['cotacoes_transacoes'],
            'movimentacoes_transacoes': dashboard['movimentacoes_transacoes'],
        }

    def build_context(self, carteira: str) -> dict:
        """
        Monta o context para o template
        """
        context = {'cotacao_dia': self.cotacao_dia}
        context.update(self.get_wallet_context(carteira))
        context.update(self.get_financeiro_context())
        context.update(self.get_btc_context())
        return context