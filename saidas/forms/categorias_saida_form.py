from django import forms

from saidas.models import Categorias_Saidas

class Categorias_SaidasForm(forms.ModelForm):
    class Meta:
        model = Categorias_Saidas
        fields = ['nome']

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ex: Alimentação',
            }),
        }

        labels = {
            'nome': 'Nome',
        }