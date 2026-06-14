from rest_framework import viewsets, permissions
from saidas.models import Saidas, Categorias_Saidas
from saidas.serializer.saida_serializer import SaidaSerializer, CategoriaSaidaSerializer


class CategoriaSaidaViewSet(viewsets.ModelViewSet):
    """
    Possibilita o usuário utilizar categorias de gastos
    """
    serializer_class = CategoriaSaidaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Categorias_Saidas.objects.filter(usuario=self.request.user)

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)


class SaidaViewSet(viewsets.ModelViewSet):
    """
    Permite o usuário gerenciar seus gastos
    """
    serializer_class = SaidaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Saidas.objects.filter(usuario=self.request.user).order_by('-data')

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)