import pytest
from entradas.test.factory.factory import EntradaFactory
from usuarios.test.factory.factory import UsuarioFactory


@pytest.mark.django_db
class TestEntradaModel:

    def test_criacao_entrada(self):
        entrada = EntradaFactory(valor=1500.00)
        assert entrada.pk is not None
        assert entrada.valor == 1500.00

    def test_entrada_pertence_ao_usuario(self):
        
        usuario = UsuarioFactory()
        entrada = EntradaFactory(usuario=usuario)
        assert entrada.usuario == usuario

    def test_str_entrada(self):
        entrada = EntradaFactory()
        assert str(entrada) is not None