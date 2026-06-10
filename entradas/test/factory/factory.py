import factory
from entradas.models import Entradas, Categorias_Entradas
from usuarios.test.factory.factory import UsuarioFactory
import datetime


class CategoriaEntradaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Categorias_Entradas

    usuario = factory.SubFactory(UsuarioFactory)
    nome = factory.Sequence(lambda n: f'Categoria Entrada {n}')


class EntradaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Entradas

    usuario = factory.SubFactory(UsuarioFactory)
    categoria = factory.SubFactory(CategoriaEntradaFactory)
    data = factory.LazyFunction(datetime.date.today)
    valor = 1000.00
    descricao = factory.Sequence(lambda n: f'Entrada {n}')