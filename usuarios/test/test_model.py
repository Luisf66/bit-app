import pytest
from saidas.test.factory.factory import SaidaFactory
from entradas.test.factory.factory import EntradaFactory
from usuarios.test.factory.factory import UsuarioFactory
from bitcoin.test.factory.factory import TransacaoBTCFactory


@pytest.mark.django_db
class TestUsuarioModel:

    def test_criacao_usuario(self):
        usuario = UsuarioFactory()
        assert usuario.pk is not None
        assert usuario.username.startswith('usuario_')

    def test_str_usuario(self):
        usuario = UsuarioFactory(username='testuser')
        assert str(usuario) == 'testuser'



@pytest.mark.django_db
class TestIsolamentoUsuarios:
    """Garante que dados de um usuário não vazam para outro."""

    def test_entradas_isoladas(self):
        usuario1 = UsuarioFactory()
        usuario2 = UsuarioFactory()
        EntradaFactory(usuario=usuario1)
        EntradaFactory(usuario=usuario1)
        EntradaFactory(usuario=usuario2)

        from entradas.models import Entradas
        assert Entradas.objects.filter(usuario=usuario1).count() == 2
        assert Entradas.objects.filter(usuario=usuario2).count() == 1

    def test_saidas_isoladas(self):
        usuario1 = UsuarioFactory()
        usuario2 = UsuarioFactory()
        SaidaFactory(usuario=usuario1)
        SaidaFactory(usuario=usuario2)
        SaidaFactory(usuario=usuario2)

        from saidas.models import Saidas
        assert Saidas.objects.filter(usuario=usuario1).count() == 1
        assert Saidas.objects.filter(usuario=usuario2).count() == 2

    def test_transacoes_btc_isoladas(self):
        usuario1 = UsuarioFactory()
        usuario2 = UsuarioFactory()
        TransacaoBTCFactory(usuario=usuario1)
        TransacaoBTCFactory(usuario=usuario2)

        from bitcoin.models import TransacaoBTC
        assert TransacaoBTC.objects.filter(usuario=usuario1).count() == 1
        assert TransacaoBTC.objects.filter(usuario=usuario2).count() == 1