from django import forms
from entradas.models import Categorias_Entradas

class Categorias_EntradasForm(forms.ModelForm):
    class Meta:
        model = Categorias_Entradas
        fields = [
            'nome',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ex: Alimentação',
            }),
        }

        labels = {
            'nome': 'Nome',
        }