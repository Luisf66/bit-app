import json
import requests
from ai import prompt
from ai.models import Prompt
from bitcoin.service.dashboard_service import DashboardService

from decouple import config


class BitAppAgent:
    def __init__(self):
        self.__base_url = config('AI_BASE_URL')
        self.__model = config('AI_MODEL')
        self.__api_key = config('AI_API_KEY')  # 🔑 novo

    def __get_data(self):
       """
       Obtem os dados do dashboard para enviar para IA analisar
       """
       dashboard_service = DashboardService()

       return json.dumps({
           # gastos do usuario
           'total_saidas': dashboard_service.get_financeiro_context()['total_saidas'],
           'data_saida': dashboard_service.get_financeiro_context()['data_saida'],
           'valor_saida': dashboard_service.get_financeiro_context()['valor_saida'],
           # ganhos do usuario
           'total_entradas': dashboard_service.get_financeiro_context()['total_entradas'],
           'data_entrada': dashboard_service.get_financeiro_context()['data_entrada'],
           'valor_entrada': dashboard_service.get_financeiro_context()['valor_entrada'],
           # saldo do usuario
           'saldo': dashboard_service.get_financeiro_context()['saldo'],
           # compra e envio de BTC na BIPA
           'total_gasto_btc': dashboard_service.get_btc_context()['total_gasto_btc'],
           'total_liquido_btc': dashboard_service.get_btc_context()['total_liquido_btc'],
       })


    def invoke(self):
        
        payload = {
            "model": self.__model,
            "messages": [
                {
                    "role": "system",
                    "content": prompt.SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt.USER_PROMPT.replace('{{data}}', self.__get_data()),
                }
            ],
            "stream": False
        }

        headers = {
            "Authorization": f"Bearer {self.__api_key}",  # 🔑 novo
            "Content-Type": "application/json"
        }

        #print(f'Payload: {payload}')
        
        response = requests.post(self.__base_url, json=payload, headers=headers)
        response.raise_for_status()

        # ✅ Formato OpenAI: choices[0].message.content
        result = response.json()["choices"][0]["message"]["content"]
        #print(f'Resultado: {result}')
        Prompt.objects.create(response=result)

        return result