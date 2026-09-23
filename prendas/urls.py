"""
ENRUTAMIENTO LOCAL DE LA APLICACIÓN 'PRENDAS'
Módulo: prendas/urls.py
Descripción: Define las rutas URL específicas para el catálogo y el CRUD de prendas.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('catalogo/', views.prenda_list, name='prenda_list'),
    path('catalogo/nueva/', views.prenda_create, name='prenda_create'),
    path('catalogo/editar/<int:pk>/', views.prenda_update, name='prenda_update'),
    path('catalogo/eliminar/<int:pk>/', views.prenda_delete, name='prenda_delete'),
]
