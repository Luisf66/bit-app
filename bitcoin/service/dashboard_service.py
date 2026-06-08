from app import metrics
from .blockchain_service import BlockchainService, BlockchainAPIError


class DashboardService:

    def __init__(self, usuario):
        self.usuario = usuario
        self.blockchain = BlockchainService()
        self.cotacao_dia = self.blockchain.get_btc_price()

    def get_wallet_context(self, carteira: str) -> dict:
        carteira = carteira.strip()
        informacoes_carteira = None
        saldo_btc_brl = 0

        if carteira:
            try:
                informacoes_carteira = self.blockchain.get_wallet_info(carteira)
                cotacao_float = self.blockchain.get_btc_price_float()
                saldo_btc_brl = round(
                    informacoes_carteira['saldo_btc'] * cotacao_float, 2
                )
            except BlockchainAPIError as e:
                informacoes_carteira = {'erro': str(e)}

        return {
            'carteira_buscada': carteira,
            'informacoes_carteira': informacoes_carteira,
            'saldo_btc_brl': saldo_btc_brl,
        }

    def get_financeiro_context(self) -> dict:
        saldo = metrics.obter_saldo(self.usuario)
        info = metrics.obter_informacoes_financeiras(self.usuario)
        preco_medio = metrics.obter_preco_medio(self.usuario)

        return {
            'total_saidas': saldo['total_saidas'],
            'total_entradas': saldo['total_entradas'],
            'saldo': saldo['saldo'],
            'preco_medio': preco_medio,
            'data_entrada': info['data_entrada'],
            'valor_entrada': info['valor_entrada'],
            'valor_entrada_acumulada': info['valor_entrada_acumulada'],
            'data_saida': info['data_saida'],
            'valor_saida': info['valor_saida'],
        }

    def get_btc_context(self) -> dict:
        metricas = metrics.obter_metricas(self.usuario)
        dashboard = metrics.obter_dashboard(self.usuario)

        return {
            'total_gasto_btc': metricas['total_gasto_btc'],
            'total_liquido_btc': metricas['total_liquido_btc'],
            'taxas_pagas_compra': metricas['taxas_pagas_compra'],
            'envio_btc_total': metricas['envio_btc_total'],
            'envio_btc_liquido': metricas['envio_btc_liquido'],
            'taxas_pagas_envio': metricas['taxas_pagas_envio'],
            'total_satoshis_comprados': metricas['total_satoshis_comprados'],
            'total_satoshis_enviados': metricas['total_satoshis_enviados'],
            'datas_transacoes': list(dashboard['datas_transacoes']),
            'tipos_transacoes': list(dashboard['tipos_transacoes']),
            'valores_transacoes': [float(v) for v in dashboard['valores_transacoes']],
            'satoshis_transacoes': [float(s) for s in dashboard['satoshis_transacoes']],
            'cotacoes_transacoes': [float(c) for c in dashboard['cotacoes_transacoes']],
            'movimentacoes_transacoes': list(dashboard['movimentacoes_transacoes']),
        }

    def build_context(self, carteira: str) -> dict:
        context = {'cotacao_dia': self.cotacao_dia}
        context.update(self.get_wallet_context(carteira))
        context.update(self.get_financeiro_context())
        context.update(self.get_btc_context())
        return context