from . import views

from django.urls import path
#from django.conf import settings
#from django.conf.urls.static import static 


app_name = 'bitcoin'

urlpatterns = [
    path('upload/', views.Bitcoin_UploadView, name='bitcoin-upload'),
    #path('dashboard/', views.DashboardView, name='dashboard'),
]

#urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)