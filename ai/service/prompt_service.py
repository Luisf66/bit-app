from datetime import timedelta
from django.utils import timezone
from ai.models import Prompt
from ai.agent import BitAppAgent

CACHE_DIAS = 7


class PromptService:

    def __init__(self, usuario):
        self.usuario = usuario

    def obter_ultimo(self) -> Prompt | None:
        return Prompt.objects.filter(
            usuario=self.usuario
        ).order_by('-created_at').first()

    def ainda_valido(self) -> bool:
        ultimo = self.obter_ultimo()
        if not ultimo:
            return False
        return (timezone.now() - ultimo.created_at) < timedelta(days=CACHE_DIAS)

    def gerar(self) -> str:
        return BitAppAgent(self.usuario).invoke()