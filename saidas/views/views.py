from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from saidas.models import Categorias_Saidas
from saidas.forms.categorias_saida_form import Categorias_SaidasForm

from saidas.models import Saidas
from saidas.forms.saida_form import SaidasForm


# Create your views here.
class Categorias_SaidasCreateView(LoginRequiredMixin, CreateView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_create.html'
    form_class = Categorias_SaidasForm
    success_url = reverse_lazy('saidas:categorias-saidas-list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class Categorias_SaidasListView(LoginRequiredMixin, ListView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_list.html'
    context_object_name = 'categorias_saidas'

    def get_queryset(self):
        return Categorias_Saidas.objects.filter(usuario=self.request.user)

class Categorias_SaidasUpdateView(LoginRequiredMixin, UpdateView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_update.html'
    form_class = Categorias_SaidasForm
    success_url = reverse_lazy('saidas:categorias-saidas-list')

    def get_queryset(self):
        return Categorias_Saidas.objects.filter(usuario=self.request.user)

class Categorias_SaidasDeleteView(LoginRequiredMixin, DeleteView):
    model = Categorias_Saidas
    template_name = 'categorias_saidas/categorias_saidas_delete.html'
    success_url = reverse_lazy('saidas:categorias-saidas-list')

    def get_queryset(self):
        return Categorias_Saidas.objects.filter(usuario=self.request.user)

class SaidasCreateView(LoginRequiredMixin, CreateView):
    model = Saidas
    template_name = 'saidas/saidas_create.html'
    form_class = SaidasForm
    success_url = reverse_lazy('saidas:saidas-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

class SaidasListView(LoginRequiredMixin, ListView):
    model = Saidas
    template_name = 'saidas/saidas_list.html'
    context_object_name = 'saidas'
    ordering = ['data']

    def get_queryset(self):
        return Saidas.objects.filter(usuario=self.request.user)


class SaidasUpdateView(LoginRequiredMixin, UpdateView):
    model = Saidas
    template_name = 'saidas/saidas_update.html'
    form_class = SaidasForm
    success_url = reverse_lazy('saidas:saidas-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['usuario'] = self.request.user
        return kwargs

    def get_queryset(self):
        return Saidas.objects.filter(usuario=self.request.user)

class SaidasDeleteView(LoginRequiredMixin, DeleteView):
    model = Saidas
    template_name = 'saidas/saidas_delete.html'
    success_url = reverse_lazy('saidas:saidas-list')

    def get_queryset(self):
        return Saidas.objects.filter(usuario=self.request.user)
