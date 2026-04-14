from django.urls import path

from . import views

app_name = 'entradas'

urlpatterns = [
    path('category/create/', views.Categorias_EntradasCreateView.as_view(), name='categorias-entradas-create'),
    path('category/list/', views.Categorias_EntradasListView.as_view(), name='categorias-entradas-list'),
    path('category/<int:pk>/update/', views.Categorias_EntradasUpdateView.as_view(), name='categorias-entradas-update'),
    path('category/<int:pk>/delete/', views.Categorias_EntradasDeleteView.as_view(), name='categorias-entradas-delete'),

    path('create/', views.EntradasCreateView.as_view(), name='entradas-create'),
    path('list/', views.EntradasListView.as_view(), name='entradas-list'),
    path('<int:pk>/update/', views.EntradasUpdateView.as_view(), name='entradas-update'),
    path('<int:pk>/delete/', views.EntradasDeleteView.as_view(), name='entradas-delete'),
]