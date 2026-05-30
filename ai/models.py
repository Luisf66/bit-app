from django.db import models

class Prompt(models.Model):
    response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Análise IA'
        verbose_name_plural = 'Análises IA'

    def __str__(self):
        return f"Análise gerada em {self.created_at.strftime('%d/%m/%Y %H:%M')}"