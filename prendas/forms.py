"""
CAPA DE FORMULARIOS Y VALIDACIONES DE NEGOCIO (MTV - V/M INTERFACE)
Módulo: prendas/forms.py
Descripción:
    Implementa el formulario ModelForm vinculado a la entidad 'Prenda'.
    Controla la presentación de los controles HTML, la inyección de estilos
    Bootstrap 5, la traducción explícita de mensajes de error al español y
    la ejecución de validaciones de lógica de negocio (precios mayores a cero,
    stock no negativo y normalización de códigos SKU).
"""

from django import forms
from .models import Prenda


class PrendaForm(forms.ModelForm):
    """
    Formulario reactivo y tipificado basado en el modelo relacional Prenda.
    Mapea campos de base de datos a widgets HTML y aplica reglas de negocio estrictas.
    """

    class Meta:
        # Vinculación con el modelo relacional subyacente
        model = Prenda

        # Lista de atributos expuestos en los formularios web (Creación y Edición)
        fields = [
            'nombre',
            'codigo_sku',
            'categoria',
            'talla',
            'color',
            'precio',
            'stock',
            'imagen_url',
            'descripcion',
            'disponible',
        ]

        # ==============================================================================
        # SOBREESCRITURA DE MENSAJES DE ERROR AL ESPAÑOL
        # Reemplaza cualquier texto generado en inglés por validadores automáticos del modelo
        # ==============================================================================
        error_messages = {
            'stock': {
                'min_value': 'El stock disponible no puede ser un número negativo.',
                'invalid': 'Ingrese un número entero válido para las unidades de stock.',
                'required': 'El stock en bodega es un campo obligatorio.',
            },
            'precio': {
                'min_value': 'El precio del artículo debe ser estrictamente mayor a 0 ($CLP).',
                'invalid': 'Ingrese un monto numérico decimal válido para el precio.',
                'required': 'El precio unitario es un campo obligatorio.',
            },
            'codigo_sku': {
                'unique': 'Ya existe una prenda registrada con este código SKU en MariaDB.',
                'required': 'El código SKU identificador es obligatorio.',
            },
            'nombre': {
                'required': 'El nombre comercial de la prenda es obligatorio.',
                'max_length': 'El nombre no puede superar los 120 caracteres.',
            },
            'imagen_url': {
                'invalid': 'Ingrese una dirección URL directa y válida (ej. https://images.unsplash.com/...).',
            },
        }

        # ==============================================================================
        # WIDGETS Y CLASES DE RENDERIZADO VISUAL BOOTSTRAP 5
        # Define etiquetas HTML5, atributos visuales y placeholders descriptivos
        # ==============================================================================
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'Ej. Hoodie Boxy Heavyweight Washed',
            }),
            'codigo_sku': forms.TextInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'Ej. HOD-006 / POL-006',
            }),
            'categoria': forms.Select(attrs={
                'class': 'form-select rounded-0',
            }),
            'talla': forms.Select(attrs={
                'class': 'form-select rounded-0',
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'Ej. Negro Carbón, Gris Jaspeado',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': '0.00',
                'step': '100',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': '0',
                'min': '0',
            }),
            'imagen_url': forms.URLInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'https://images.unsplash.com/photo-...',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control rounded-0',
                'rows': 3,
                'placeholder': 'Describa el material textil, gramaje (gsm) y calce...',
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    # ==============================================================================
    # MÉTODOS DE VALIDACIÓN PERSONALIZADA (REGLAS DE NEGOCIO DEL NEGOCIO)
    # Se ejecutan de forma secuencial al invocar 'form.is_valid()' en views.py
    # ==============================================================================

    def clean_precio(self):
        """
        Regla de Negocio: El precio comercial debe ser estrictamente mayor a 0.
        Impide publicar prendas gratuitas o montos negativos en la boutique.
        """
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio <= 0:
            raise forms.ValidationError(
                "El precio comercial debe ser estrictamente mayor a 0 ($CLP)."
            )
        return precio

    def clean_stock(self):
        """
        Regla de Negocio: El inventario disponible no puede ser un número negativo.
        Se permite stock igual a 0 para representar un producto temporalmente agotado.
        """
        stock = self.cleaned_data.get('stock')
        if stock is not None and stock < 0:
            raise forms.ValidationError(
                "El stock disponible no puede ser un número negativo."
            )
        return stock

    def clean_codigo_sku(self):
        """
        Regla de Negocio: Normalización y saneamiento del código SKU.
        Convierte automáticamente el texto a mayúsculas y elimina espacios espurios.
        """
        sku = self.cleaned_data.get('codigo_sku')
        if sku:
            sku_limpio = sku.strip().upper()
            if len(sku_limpio) < 4:
                raise forms.ValidationError(
                    "El código SKU debe tener al menos 4 caracteres (ej. POL-001 o HOD-001)."
                )
            return sku_limpio
        return sku