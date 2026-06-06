from django.urls import reverse_lazy
from django.views.generic import CreateView
from usuarios.forms.usuario_form import RegistroForm


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'usuarios/registro.html'
    success_url = reverse_lazy('login')