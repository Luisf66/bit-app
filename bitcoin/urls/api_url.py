from rest_framework.routers import DefaultRouter
from bitcoin.views.api_views import TransacaoBTCViewSet

router = DefaultRouter()
router.register('transacoes', TransacaoBTCViewSet, basename='transacao-btc')

urlpatterns = router.urls