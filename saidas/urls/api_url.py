from rest_framework.routers import DefaultRouter
from saidas.views.api_views import SaidaViewSet, CategoriaSaidaViewSet

router = DefaultRouter()
router.register('saidas', SaidaViewSet, basename='saida')
router.register('categorias', CategoriaSaidaViewSet, basename='categoria-saida')

urlpatterns = router.urls