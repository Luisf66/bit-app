from rest_framework import serializers
from saidas.models import Saidas, Categorias_Saidas


class CategoriaSaidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias_Saidas
        fields = ['id', 'nome']


class SaidaSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Saidas
        fields = ['id', 'data', 'valor', 'descricao', 'categoria', 'categoria_nome']

    def validate_categoria(self, categoria):
        usuario = self.context['request'].user
        if categoria.usuario != usuario:
            raise serializers.ValidationError("Categoria inválida para este usuário.")
        return categoria