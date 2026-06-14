from rest_framework import serializers
from bitcoin.models import TransacaoBTC


class TransacaoBTCSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransacaoBTC
        fields = [
            'id', 'hash', 'ativo', 'movimentacao', 'tipo',
            'valor_total', 'valor_liquido', 'satoshis',
            'taxa_porcentual', 'taxa_ativo', 'taxa_quantidade',
            'cotacao_do_dia', 'origem', 'destino', 'data',
        ]
        read_only_fields = ['hash']