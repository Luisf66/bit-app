from rest_framework import serializers
from entradas.models import Entradas, Categorias_Entradas


class CategoriaEntradaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorias_Entradas
        fields = ['id', 'nome']


class EntradaSerializer(serializers.ModelSerializer):
    categoria_nome = serializers.CharField(source='categoria.nome', read_only=True)

    class Meta:
        model = Entradas
        fields = [
            'id', 
            'data', 
            'valor', 
            'descricao', 
            'categoria', 
            'categoria_nome'
        ]

    def validate_categoria(self, categoria):
        usuario = self.context['request'].user
        if categoria.usuario != usuario:
            raise serializers.ValidationError("Categoria inválida para este usuário.")
        return categoria