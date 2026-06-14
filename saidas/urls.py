from django.urls import path

from .views import views

app_name = 'saidas'

urlpatterns = [
    path('category/create/', views.Categorias_SaidasCreateView.as_view(), name='categorias-saidas-create'),
    path('category/list/', views.Categorias_SaidasListView.as_view(), name='categorias-saidas-list'),
    path('category/<int:pk>/update/', views.Categorias_SaidasUpdateView.as_view(), name='categorias-saidas-update'),
    path('category/<int:pk>/delete/', views.Categorias_SaidasDeleteView.as_view(), name='categorias-saidas-delete'),

    path('create/', views.SaidasCreateView.as_view(), name='saidas-create'),
    path('list/', views.SaidasListView.as_view(), name='saidas-list'),
    path('<int:pk>/update/', views.SaidasUpdateView.as_view(), name='saidas-update'),
    path('<int:pk>/delete/', views.SaidasDeleteView.as_view(), name='saidas-delete'),
]