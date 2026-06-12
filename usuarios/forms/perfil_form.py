from django import forms
from usuarios.models import Usuario


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'email', 'api_key_groq']
        widgets = {
            'api_key_groq': forms.PasswordInput(render_value=True),
        }
        labels = {
            'api_key_groq': 'Chave API Groq',
        }
        help_texts = {
            'api_key_groq': 'Gere sua chave em console.groq.com/keys',
        }