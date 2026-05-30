from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from saidas.models import Categorias_Saidas
from saidas.forms.categorias_saida_form import Categorias_SaidasForm

from saidas.models import Saidas
from saidas.forms.saida_form import SaidasForm


# Create your views here.
class Categorias_SaidasCreateView(CreateView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_create.html'
    form_class = Categorias_SaidasForm
    success_url = reverse_lazy('saidas:categorias-saidas-list')

class Categorias_SaidasListView(ListView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_list.html'
    context_object_name = 'categorias_saidas'

class Categorias_SaidasUpdateView(UpdateView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_update.html'
    form_class = Categorias_SaidasForm
    success_url = reverse_lazy('saidas:categorias-saidas-list')

class Categorias_SaidasDeleteView(DeleteView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_delete.html'
    success_url = reverse_lazy('saidas:categorias-saidas-list')

class SaidasCreateView(CreateView):
    model = Saidas
    template_name = 'saidas/saidas_create.html'
    form_class = SaidasForm
    success_url = reverse_lazy('saidas:saidas-list')

class SaidasListView(ListView):
    model = Saidas
    template_name = 'saidas/saidas_list.html'
    context_object_name = 'saidas'
    ordering = ['data']


class SaidasUpdateView(UpdateView):
    model = Saidas
    template_name = 'saidas/saidas_update.html'
    form_class = SaidasForm
    success_url = reverse_lazy('saidas:saidas-list')

class SaidasDeleteView(DeleteView):
    model = Saidas
    template_name = 'saidas/saidas_delete.html'
    success_url = reverse_lazy('saidas:saidas-list')