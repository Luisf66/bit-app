import requests
from django.utils.formats import number_format

# Cotação BTC/BRL

#https://blockchain.info/ticker
#https://economia.awesomeapi.com.br/last/BTC-BRL
#GET https://blockchain.info/rawaddr/{endereço_btc}
def get_btc_price():
    r = requests.get("https://blockchain.info/ticker")
    cotacao = r.json()["BRL"]["last"]
    cotacao_float = float(cotacao)
    preco_formatado = f"{cotacao_float:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    return preco_formatado

# Saldo da carteira
def get_wallet_info():
    r = requests.get(f"https://blockchain.info/rawaddr/bc1q8uzeyr5zlwzwlr9ldy8gr8gr2ys5mjxc524jwy")
    data = r.json()
    return {
        "saldo_btc": data["final_balance"] / 1e8,  # converte satoshis para BTC
        "total_transacoes": data["n_tx"],
    }