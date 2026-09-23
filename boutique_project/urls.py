"""
ENRUTAMIENTO PRINCIPAL DEL PROYECTO
Módulo: boutique_project/urls.py
Descripción: Enruta el panel de administración e incluye las URLs de la aplicación prendas.
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # Enlaza todas las rutas de la app prendas al proyecto raíz
    path('', include('prendas.urls')),
]