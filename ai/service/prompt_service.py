from datetime import timedelta
from django.utils import timezone
from ai.models import Prompt
from ai.agent import BitAppAgent


CACHE_DIAS = 7


class PromptService:

    def __init__(self, usuario):
        self.usuario = usuario

    def get_or_refresh(self) -> str:
        ultimo = Prompt.objects.filter(
            usuario=self.usuario
        ).order_by('-created_at').first()

        if ultimo and self._ainda_valido(ultimo):
            return ultimo.response

        return BitAppAgent(self.usuario).invoke()

    @staticmethod
    def _ainda_valido(prompt: Prompt) -> bool:
        diferenca = timezone.now() - prompt.created_at
        return diferenca < timedelta(days=CACHE_DIAS)