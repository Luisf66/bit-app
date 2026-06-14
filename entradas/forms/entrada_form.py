from django import forms

from entradas.models import Entradas, Categorias_Entradas


class EntradasForm(forms.ModelForm):
    class Meta:
        model = Entradas
        fields = [
            'data', 
            'valor', 
            'descricao',
            'categoria'
        ]

        widgets = {
            'data': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control form-control-sm',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select form-select-sm',
            }),
            'descricao': forms.TextInput(attrs={
                'class': 'form-control form-control-sm',
                'placeholder': 'Ex: Pagamento do salário mensal',
            }),
            'valor': forms.NumberInput(attrs={
                'class': 'form-control form-control-sm',
                'step': '0.01',
                'min': '0',
                'placeholder': '0,00',
            }),
        }

        labels = {
            'data': 'Data',
            'categoria': 'Categoria',
            'descricao': 'Descrição',
            'valor': 'Valor',
        }

    def __init__(self, *args, **kwargs):
            usuario = kwargs.pop('usuario', None)
            super().__init__(*args, **kwargs)
            if usuario:
                self.fields['categoria'].queryset = Categorias_Entradas.objects.filter(usuario=usuario)
