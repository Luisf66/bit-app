import requests
from requests.exceptions import RequestException, Timeout


class BlockchainAPIError(Exception):
    """Erro de comunicação com a Blockchain.info API."""


class BlockchainService:
    
    BASE_URL = "https://blockchain.info"
    TIMEOUT = 20  # segundos

    # ------------------------------------------------------------------ #
    #  Cotação BTC/BRL                                                     #
    # ------------------------------------------------------------------ #

    def get_btc_price(self) -> str:
        """Retorna o preço atual do BTC em BRL formatado (ex: 3.450.000,00)."""
        data = self._fetch(f"{self.BASE_URL}/ticker")
        cotacao = float(data["BRL"]["last"])
        return self._format_brl(cotacao)

    def get_btc_price_float(self) -> float:
        """Retorna o preço atual do BTC em BRL como float — útil para cálculos."""
        data = self._fetch(f"{self.BASE_URL}/ticker")
        return float(data["BRL"]["last"])

    # ------------------------------------------------------------------ #
    #  Carteira                                                            #
    # ------------------------------------------------------------------ #

    def get_wallet_info(self, address: str) -> dict:
        """
        Retorna saldo e total de transações de um endereço BTC.
        Levanta BlockchainAPIError se o endereço for inválido.
        """
        address = address.strip()
        data = self._fetch(f"{self.BASE_URL}/rawaddr/{address}")

        if 'final_balance' not in data:
            raise BlockchainAPIError("Endereço inválido ou sem dados disponíveis.")

        return {
            "saldo_btc": data["final_balance"] / 1e8,  # satoshis → BTC
            "total_transacoes": data["n_tx"],
        }

    # ------------------------------------------------------------------ #
    #  Privados                                                            #
    # ------------------------------------------------------------------ #

    def _fetch(self, url: str) -> dict:
        """Centraliza as chamadas HTTP com tratamento de erros."""
        try:
            response = requests.get(url, timeout=self.TIMEOUT)
            response.raise_for_status()
            return response.json()
        except Timeout:
            raise BlockchainAPIError(f"Timeout ao acessar: {url}")
        except RequestException as e:
            raise BlockchainAPIError(f"Erro na requisição: {e}")

    @staticmethod
    def _format_brl(valor: float) -> str:
        """Formata um float para o padrão brasileiro (3.450.000,00)."""
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")