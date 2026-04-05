from django import forms
from entradas.models import Categorias_Entradas

class Categorias_EntradasForm(forms.ModelForm):
    class Meta:
        model = Categorias_Entradas
        fields = [
            'nome',
        ]