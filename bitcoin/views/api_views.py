from rest_framework import viewsets, permissions
from bitcoin.models import TransacaoBTC
from bitcoin.serializer.bitcoin_serializer import TransacaoBTCSerializer


class TransacaoBTCViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only — transações são criadas via upload de CSV, não pela API."""
    serializer_class = TransacaoBTCSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return TransacaoBTC.objects.filter(usuario=self.request.user).order_by('-data')