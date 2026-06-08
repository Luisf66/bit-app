import factory
from saidas.models import Saidas, Categorias_Saidas
from usuarios.test.factory.factory import UsuarioFactory
import datetime


class CategoriaSaidaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categorias_Saidas

    usuario = factory.SubFactory(UsuarioFactory)
    nome = factory.Sequence(lambda n: f'Categoria Saida {n}')


class SaidaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Saidas

    usuario = factory.SubFactory(UsuarioFactory)
    categoria = factory.SubFactory(CategoriaSaidaFactory)
    data = factory.LazyFunction(datetime.date.today)
    valor = 500.00
    descricao = factory.Sequence(lambda n: f'Saida {n}')
