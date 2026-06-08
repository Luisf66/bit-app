from django.db import models
from django.conf import settings


class Prompt(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Análise IA'
        verbose_name_plural = 'Análises IA'

    def __str__(self):
        return f"Análise gerada em {self.created_at.strftime('%d/%m/%Y %H:%M')}"