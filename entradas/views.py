from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.deletion import ProtectedError
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from entradas.models import Categorias_Entradas
from entradas.forms.categorias_entrada import Categorias_EntradasForm

from entradas.models import Entradas
from entradas.forms.entrada_form import EntradasForm
# Create your views here.


class Categorias_EntradasCreateView(CreateView):
    model = Categorias_Entradas
    form_class = Categorias_EntradasForm
    template_name = 'categorias_entrada/categorias_entradas_create.html'
    success_url = reverse_lazy('entradas:categorias-entradas-list')

class Categorias_EntradasListView(ListView):
    model = Categorias_Entradas
    template_name = 'categorias_entrada/categorias_entradas_list.html'
    context_object_name = 'categorias_entradas'

class Categorias_EntradasUpdateView(UpdateView):
    model = Categorias_Entradas
    form_class = Categorias_EntradasForm
    template_name = 'categorias_entrada/categorias_entradas_update.html'
    success_url = reverse_lazy('entradas:categorias-entradas-list')

class Categorias_EntradasDeleteView(DeleteView):
    model = Categorias_Entradas
    template_name = 'categorias_entrada/categorias_entradas_delete.html'
    success_url = reverse_lazy('entradas:categorias-entradas-list')

class EntradasCreateView(CreateView):
    model = Entradas
    form_class = EntradasForm
    template_name = 'entradas_create.html'
    success_url = reverse_lazy('entradas:entradas-list')

'''    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categorias_entradas'] = Categorias_Entradas.objects.all()
        return context
'''
class EntradasListView(ListView):
    model = Entradas
    template_name = 'entradas_list.html'
    context_object_name = 'entradas'

class EntradasUpdateView(UpdateView):
    model = Entradas
    form_class = EntradasForm
    template_name = 'entradas_update.html'
    success_url = reverse_lazy('entradas:entradas-list')

class EntradasDeleteView(DeleteView):
    model = Entradas
    template_name = 'entradas_delete.html'
    success_url = reverse_lazy('entradas:entradas-list')

    def delete(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            messages.error(request, f"Erro ao excluir: {e.protected_objects}")
            return redirect(self.success_url)