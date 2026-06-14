from bitcoin.views import views

from django.urls import path
#from django.conf import settings
#from django.conf.urls.static import static 


app_name = 'bitcoin'

urlpatterns = [
    path('upload/', views.bitcoin_upload_view, name='bitcoin-upload'),
    path('list/', views.TransacaoListView.as_view(), name='bitcoin-list'),
    path('dashboard/', views.dashboard_view, name='bitcoin-dashboard'),
    path('dashboard/analise/', views.gerar_analise_view, name='gerar-analise'),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)