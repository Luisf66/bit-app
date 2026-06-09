import pytest
from django.urls import reverse
from usuarios.test.factory.factory import UsuarioFactory
from entradas.test.factory.factory import EntradaFactory, CategoriaEntradaFactory


@pytest.mark.django_db
class TestEntradasViewsAutenticacao:
    """Garante que views redirecionam para login sem autenticação."""

    def test_list_requer_login(self, client):
        response = client.get(reverse('entradas:entradas-list'))
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_create_requer_login(self, client):
        response = client.get(reverse('entradas:entradas-create'))
        assert response.status_code == 302

    def test_update_requer_login(self, client):
        entrada = EntradaFactory()
        response = client.get(reverse('entradas:entradas-update', args=[entrada.pk]))
        assert response.status_code == 302

    def test_delete_requer_login(self, client):
        entrada = EntradaFactory()
        response = client.get(reverse('entradas:entradas-delete', args=[entrada.pk]))
        assert response.status_code == 302


@pytest.mark.django_db
class TestEntradasViewsIsolamento:
    """Garante que usuário só vê seus próprios dados."""

    def test_list_exibe_apenas_entradas_do_usuario(self, client):
        usuario1 = UsuarioFactory()
        usuario2 = UsuarioFactory()
        cat1 = CategoriaEntradaFactory(usuario=usuario1)
        cat2 = CategoriaEntradaFactory(usuario=usuario2)
        EntradaFactory(usuario=usuario1, categoria=cat1, descricao='Entrada user1')
        EntradaFactory(usuario=usuario2, categoria=cat2, descricao='Entrada user2')

        client.force_login(usuario1)
        response = client.get(reverse('entradas:entradas-list'))

        assert response.status_code == 200
        entradas = response.context['entradas']
        assert entradas.count() == 1
        assert entradas.first().usuario == usuario1

    def test_usuario_nao_acessa_entrada_de_outro(self, client):
        usuario1 = UsuarioFactory()
        usuario2 = UsuarioFactory()
        cat2 = CategoriaEntradaFactory(usuario=usuario2)
        entrada_usuario2 = EntradaFactory(usuario=usuario2, categoria=cat2)

        client.force_login(usuario1)
        response = client.get(
            reverse('entradas:entradas-update', args=[entrada_usuario2.pk])
        )
        assert response.status_code == 404

    def test_criar_entrada_associa_usuario(self, client):
        usuario = UsuarioFactory()
        categoria = CategoriaEntradaFactory(usuario=usuario)

        client.force_login(usuario)
        client.post(reverse('entradas:entradas-create'), {
            'data': '2025-01-01',
            'valor': '1000.00',
            'descricao': 'Salário',
            'categoria': categoria.pk,
        })

        from entradas.models import Entradas
        entrada = Entradas.objects.get(usuario=usuario)
        assert entrada.usuario == usuario