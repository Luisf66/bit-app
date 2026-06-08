from django.db import models
from django.contrib.auth.models import AbstractUser


class Usuario(AbstractUser):
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    def __str__(self):
        return self.username