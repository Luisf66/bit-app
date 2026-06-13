import json
import requests
from ai import prompt
from ai.models import Prompt
from bitcoin.service.dashboard_service import DashboardService
from decouple import config


class BitAppAgent:

    def __init__(self, usuario):
        self.usuario = usuario
        self.__base_url = config('AI_BASE_URL')   # ← URL da IA
        self.__model = config('AI_MODEL')         # ← Modelo da LLM
        self.__api_key = usuario.api_key_groq     # ← chave do usuário

    def __get_data(self):
        """
        Obtém os dados do dashboard do usuário para enviar para a IA analisar.
        """
        dashboard_service = DashboardService(self.usuario)
        financeiro = dashboard_service.get_financeiro_context()
        btc = dashboard_service.get_btc_context()

        return json.dumps({
            'total_saidas': financeiro['total_saidas'],
            'data_saida': financeiro['data_saida'],
            'valor_saida': financeiro['valor_saida'],
            'total_entradas': financeiro['total_entradas'],
            'data_entrada': financeiro['data_entrada'],
            'valor_entrada': financeiro['valor_entrada'],
            'saldo': financeiro['saldo'],
            'total_gasto_btc': btc['total_gasto_btc'],
            'total_liquido_btc': btc['total_liquido_btc'],
        }, default=str)

    def invoke(self) -> str:
        if not self.usuario.tem_api_key():
            raise ValueError(
                'Você precisa cadastrar sua chave API da Groq no perfil para usar a análise de IA.'
            )
        payload = {
            "model": self.__model,
            "messages": [
                {"role": "system", "content": prompt.SYSTEM_PROMPT},
                {"role": "user", "content": prompt.USER_PROMPT.replace('{{data}}', self.__get_data())},
            ],
            "stream": False
        }
        headers = {
            "Authorization": f"Bearer {self.__api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(self.__base_url, json=payload, headers=headers)
        response.raise_for_status()

        result = response.json()["choices"][0]["message"]["content"]

        Prompt.objects.create(response=result, usuario=self.usuario)

        return result