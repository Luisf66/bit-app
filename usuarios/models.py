from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    criado_em = models.DateTimeField(auto_now_add=True)
    api_key_groq = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Chave API Groq'
    )

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username
    
    def tem_api_key(self) -> bool:
        return bool(self.api_key_groq)