from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models.deletion import ProtectedError
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from entradas.models import Categorias_Entradas
from entradas.forms.categorias_entrada_form import Categorias_EntradasForm

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

    def post(self, request, *args, **kwargs):
        try:
            return super().delete(request, *args, **kwargs)
        except ProtectedError as e:
            for obj in e.protected_objects:
                messages.error(request, f"A categoria está sendo usada por : {obj}")
            return redirect(self.success_url)

class EntradasCreateView(CreateView):
    model = Entradas
    form_class = EntradasForm
    template_name = 'entradas/entradas_create.html'
    success_url = reverse_lazy('entradas:entradas-list')

class EntradasListView(ListView):
    model = Entradas
    template_name = 'entradas/entradas_list.html'
    context_object_name = 'entradas'
    ordering = ['data']

class EntradasUpdateView(UpdateView):
    model = Entradas
    form_class = EntradasForm
    template_name = 'entradas/entradas_update.html'
    success_url = reverse_lazy('entradas:entradas-list')

class EntradasDeleteView(DeleteView):
    model = Entradas
    template_name = 'entradas/entradas_delete.html'
    success_url = reverse_lazy('entradas:entradas-list')