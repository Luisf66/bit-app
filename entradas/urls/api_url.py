from rest_framework.routers import DefaultRouter
from entradas.views.api_views import EntradaViewSet, CategoriaEntradaViewSet

router = DefaultRouter()
router.register('entradas', EntradaViewSet, basename='entrada')
router.register('categorias', CategoriaEntradaViewSet, basename='categoria-entrada')

urlpatterns = router.urls