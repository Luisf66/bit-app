from rest_framework import viewsets, permissions
from entradas.models import Entradas, Categorias_Entradas
from entradas.serializer.entrada_serializer import EntradaSerializer, CategoriaEntradaSerializer


class CategoriaEntradaViewSet(viewsets.ModelViewSet):
    """
    Possibilita o usuário utilizar categorias de entradas
    """
    serializer_class = CategoriaEntradaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Categorias_Entradas.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class EntradaViewSet(viewsets.ModelViewSet):
    """
    Gerencia as entradas do usuário autenticado
    """
    serializer_class = EntradaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Entradas.objects.filter(usuario=self.request.user).order_by('-data')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        return context