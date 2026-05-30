from datetime import timedelta
from django.utils import timezone
from ai.models import Prompt
from ai.agent import BitAppAgent


CACHE_DIAS = 7


class PromptService:

    def get_or_refresh(self) -> str:
        """
        Retorna a análise mais recente se tiver menos de 7 dias.
        Caso contrário, requisita uma nova análise à IA e salva no banco.
        """
        ultimo = Prompt.objects.order_by('-created_at').first()

        if ultimo and self._ainda_valido(ultimo):
            return ultimo.response

        return BitAppAgent().invoke()

    # ------------------------------------------------------------------ #
    #  Privado                                                             #
    # ------------------------------------------------------------------ #

    @staticmethod
    def _ainda_valido(prompt: Prompt) -> bool:
        diferenca = timezone.now() - prompt.created_at
        return diferenca < timedelta(days=CACHE_DIAS)