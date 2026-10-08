"""
CAPA DE FORMULARIOS Y VALIDACIONES DE NEGOCIO (MTV - V/M INTERFACE)
Módulo: prendas/forms.py
Descripción:
    Implementa el formulario ModelForm vinculado a la entidad 'Prenda'.
    Aplica reglas de negocio estrictas: validación de longitud para nombre,
    formato regex exacto de 7 caracteres para SKU con control de duplicados,
    rango de stock (0 a 333) con cambio automático a no disponible/agotado,
    rango de precio ($1.000 a $111.111), control de color y descripción.
"""

import re
from django import forms
from .models import Prenda


class PrendaForm(forms.ModelForm):
    """
    Formulario reactivo y tipificado basado en el modelo relacional Prenda.
    Aplica reglas de negocio estrictas tanto a nivel visual como en el backend.
    """

    class Meta:
        model = Prenda
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

        error_messages = {
            'stock': {
                'min_value': 'El stock disponible no puede ser un número negativo.',
                'invalid': 'Ingrese un número entero válido para las unidades de stock.',
                'required': 'El stock en bodega es un campo obligatorio.',
            },
            'precio': {
                'min_value': 'El precio del artículo debe ser al menos de $1.000 CLP.',
                'invalid': 'Ingrese un monto numérico válido para el precio.',
                'required': 'El precio unitario es un campo obligatorio.',
            },
            'codigo_sku': {
                'unique': 'Este código SKU ya se encuentra registrado en el catálogo.',
                'required': 'El código SKU identificador es obligatorio.',
            },
            'nombre': {
                'required': 'El nombre comercial de la prenda es obligatorio.',
            },
            'imagen_url': {
                'invalid': 'Ingrese una dirección URL directa y válida (ej. https://images.unsplash.com/...).',
            },
        }

        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'Ej. Polera Oversize Heavyweight Algodón Peinado Negra',
                'minlength': '30',
                'maxlength': '60',
            }),
            'codigo_sku': forms.TextInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'Ej. POL-003 o HOD-003',
                'minlength': '7',
                'maxlength': '7',
                'style': 'text-transform: uppercase;',
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
                'minlength': '3',
                'maxlength': '30',
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'Ej. 19990',
                'min': '1000',
                'max': '111111',
                'step': '1',
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': '0 a 333',
                'min': '0',
                'max': '333',
            }),
            'imagen_url': forms.URLInput(attrs={
                'class': 'form-control rounded-0',
                'placeholder': 'https://images.unsplash.com/...',
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control rounded-0',
                'rows': 3,
                'placeholder': 'Describa el material textil, gramaje y calce...',
                'minlength': '20',
                'maxlength': '250',
            }),
            'disponible': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            nombre = ' '.join(nombre.strip().split())
            longitud = len(nombre)
            if longitud < 30 or longitud > 60:
                raise forms.ValidationError(
                    f"El nombre debe contener entre 30 y 60 caracteres (actualmente tiene {longitud}). "
                    "Incluya tipo de prenda, atributos, corte o color descriptivo."
                )
        return nombre

    def clean_codigo_sku(self):
        sku = self.cleaned_data.get('codigo_sku')
        if sku:
            sku_limpio = sku.strip().upper()
            patron = r'^(POL|HOD)-\d{3}$'
            if not re.match(patron, sku_limpio):
                raise forms.ValidationError(
                    "El SKU debe tener exactamente 7 caracteres en formato POL-XXX o HOD-XXX "
                    "(donde XXX es un número correlativo de 3 dígitos, ej. POL-003)."
                )

            consulta = Prenda.objects.filter(codigo_sku=sku_limpio)
            if self.instance and self.instance.pk:
                consulta = consulta.exclude(pk=self.instance.pk)

            if consulta.exists():
                raise forms.ValidationError(
                    f"El código SKU '{sku_limpio}' ya se encuentra registrado en el catálogo. "
                    "Ingrese un correlativo diferente para evitar duplicidad."
                )

            return sku_limpio
        return sku

    def clean_color(self):
        color = self.cleaned_data.get('color')
        if color:
            color = ' '.join(color.strip().split())
            if len(color) < 3 or len(color) > 30:
                raise forms.ValidationError(
                    f"El color debe contener entre 3 y 30 caracteres (actualmente tiene {len(color)})."
                )
            if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑ\s]+$', color):
                raise forms.ValidationError("El color solo puede contener letras y espacios.")
        return color

    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock is not None:
            if stock < 0:
                raise forms.ValidationError("El stock disponible no puede ser un número negativo.")
            if stock > 333:
                raise forms.ValidationError(
                    f"El stock ingresado ({stock}) excede el tope máximo permitido de 333 unidades."
                )
        return stock

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None:
            if precio < 1000:
                raise forms.ValidationError("El precio comercial debe ser de al menos $1.000 CLP.")
            if precio > 111111:
                raise forms.ValidationError(
                    f"El precio (${int(precio):,}) supera el tope máximo permitido de $111.111 CLP."
                )
        return precio

    def clean_descripcion(self):
        descripcion = self.cleaned_data.get('descripcion')
        if descripcion:
            descripcion = ' '.join(descripcion.strip().split())
            longitud = len(descripcion)
            if longitud < 20 or longitud > 250:
                raise forms.ValidationError(
                    f"La descripción debe contener entre 20 y 250 caracteres (actualmente tiene {longitud})."
                )
        return descripcion

    def clean(self):
        cleaned_data = super().clean()
        stock = cleaned_data.get('stock')
        if stock == 0:
            cleaned_data['disponible'] = False
        return cleaned_data