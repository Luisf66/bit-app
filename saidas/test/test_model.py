import pytest
from saidas.test.factory.factory import SaidaFactory
from usuarios.test.factory.factory import UsuarioFactory

@pytest.mark.django_db
class TestSaidaModel:

    def test_criacao_saida(self):
        saida = SaidaFactory(valor=300.00)
        assert saida.pk is not None
        assert saida.valor == 300.00

    def test_saida_pertence_ao_usuario(self):
        usuario = UsuarioFactory()
        saida = SaidaFactory(usuario=usuario)
        assert saida.usuario == usuario
