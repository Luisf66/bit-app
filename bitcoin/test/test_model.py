import pytest
from bitcoin.test.factory.factory import TransacaoBTCFactory
from usuarios.test.factory.factory import UsuarioFactory

@pytest.mark.django_db
class TestTransacaoBTCModel:

    def test_criacao_transacao(self):
        transacao = TransacaoBTCFactory()
        assert transacao.pk is not None
        assert transacao.ativo == 'BTC'

    def test_hash_unico(self):
        t1 = TransacaoBTCFactory()
        t2 = TransacaoBTCFactory()
        assert t1.hash != t2.hash

    def test_transacao_pertence_ao_usuario(self):
        usuario = UsuarioFactory()
        transacao = TransacaoBTCFactory(usuario=usuario)
        assert transacao.usuario == usuario