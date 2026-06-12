from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from usuarios.forms.perfil_form import PerfilForm
from usuarios.forms.usuario_form import RegistroForm


class RegistroView(CreateView):
    form_class = RegistroForm
    template_name = 'registro.html'
    success_url = reverse_lazy('usuarios:login')

@login_required
def perfil_view(request):
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil atualizado com sucesso.')
            return redirect('bitcoin:bitcoin-dashboard')
    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'perfil.html', {'form': form})