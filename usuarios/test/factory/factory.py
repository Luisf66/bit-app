import factory
from django.contrib.auth import get_user_model


Usuario = get_user_model()

class UsuarioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Usuario
        #skip_postgeneration_save = True  # ← remove o DeprecationWarning

    username = factory.Sequence(lambda n: f'usuario_{n}')
    email = factory.Sequence(lambda n: f'usuario_{n}@email.com')
    password = factory.PostGenerationMethodCall('set_password', 'senha123')