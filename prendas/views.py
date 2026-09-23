"""
CAPA VIEW (V) - CONTROLADOR Y LÓGICA DE NEGOCIO
Módulo: prendas/views.py
Descripción:
    Implementa las funciones controladoras para el ciclo completo CRUD:
      - Portada de inicio con productos destacados (home)
      - Catálogo general con filtros por categoría Poleras/Hoodies (prenda_list)
      - Registro de nueva prenda con validaciones (prenda_create)
      - Edición de prenda existente (prenda_update)
      - Confirmación y eliminación física del registro (prenda_delete)
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Prenda
from .forms import PrendaForm

def home(request):
    """Renderiza la vitrina inicial con los productos más recientes del inventario."""
    destacados = Prenda.objects.filter(disponible=True)[:6]
    return render(request, 'prendas/index.html', {'destacados': destacados})

def prenda_list(request):
    """
    Lista el catálogo completo o filtrado según la categoría seleccionada
    (Poleras o Hoodies), consumiendo los datos mediante el ORM de Django.
    """
    categoria = request.GET.get('categoria')
    if categoria in [Prenda.CATEGORIA_POLERA, Prenda.CATEGORIA_HOODIE]:
        prendas = Prenda.objects.filter(categoria=categoria)
    else:
        prendas = Prenda.objects.all()

    contexto = {
        'prendas': prendas,
        'categoria_seleccionada': categoria,
    }
    return render(request, 'prendas/prenda_list.html', contexto)

def prenda_create(request):
    """Procesa el formulario de registro de nuevas prendas con mensajes de retroalimentación."""
    if request.method == 'POST':
        form = PrendaForm(request.POST)
        if form.is_valid():
            prenda = form.save()
            messages.success(request, f"Prenda '{prenda.nombre}' guardada exitosamente en el catálogo.")
            return redirect('prenda_list')
    else:
        form = PrendaForm()

    return render(request, 'prendas/prenda_create.html', {'form': form})

def prenda_update(request, pk):
    """Carga y actualiza una prenda existente mediante su clave primaria (pk)."""
    prenda = get_object_or_404(Prenda, pk=pk)
    if request.method == 'POST':
        form = PrendaForm(request.POST, instance=prenda)
        if form.is_valid():
            form.save()
            messages.success(request, f"Prenda '{prenda.nombre}' actualizada correctamente.")
            return redirect('prenda_list')
    else:
        form = PrendaForm(instance=prenda)

    return render(request, 'prendas/prenda_update.html', {'form': form, 'prenda': prenda})

def prenda_delete(request, pk):
    """Muestra pantalla de confirmación y elimina físicamente la prenda seleccionada."""
    prenda = get_object_or_404(Prenda, pk=pk)
    if request.method == 'POST':
        nombre_eliminado = prenda.nombre
        prenda.delete()
        messages.warning(request, f"La prenda '{nombre_eliminado}' ha sido eliminada del catálogo.")
        return redirect('prenda_list')

    return render(request, 'prendas/prenda_confirm_delete.html', {'prenda': prenda})
