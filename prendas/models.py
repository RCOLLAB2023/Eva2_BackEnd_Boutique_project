"""
CAPA MODEL (M) - ARQUITECTURA MTV DJANGO
Módulo: prendas/models.py
Descripción:
    Define la estructura de la tabla 'prendas_prenda' en la base de datos MySQL/MariaDB.
    Representa la entidad asignada 'Prenda' para la Boutique de Ropa.
"""

from django.db import models
from django.core.validators import MinValueValidator

class Prenda(models.Model):
    """
    Entidad principal de la boutique.
    Contempla únicamente las categorías requeridas: Poleras y Hoodies.
    """

    # Constantes representativas de categorías
    CATEGORIA_POLERA = 'Poleras'
    CATEGORIA_HOODIE = 'Hoodies'

    OPCIONES_CATEGORIA = [
        (CATEGORIA_POLERA, 'Poleras'),
        (CATEGORIA_HOODIE, 'Hoodies'),
    ]

    # Opciones de tallaje
    OPCIONES_TALLA = [
        ('S', 'Small (S)'),
        ('M', 'Medium (M)'),
        ('L', 'Large (L)'),
        ('XL', 'Extra Large (XL)'),
    ]

    # 1. Nombre de la prenda
    nombre = models.CharField(
        max_length=120,
        verbose_name="Nombre de la prenda",
        help_text="Ejemplo: Hoodie Oversize Essential"
    )

    # 2. Código SKU (Stock Keeping Unit): identificador único
    codigo_sku = models.CharField(
        max_length=30,
        unique=True,
        verbose_name="Código SKU",
        help_text="Identificador único del producto"
    )

    # 3. Categoría exclusiva: Poleras o Hoodies
    categoria = models.CharField(
        max_length=20,
        choices=OPCIONES_CATEGORIA,
        default=CATEGORIA_POLERA,
        verbose_name="Categoría"
    )

    # 4. Talla disponible
    talla = models.CharField(
        max_length=5,
        choices=OPCIONES_TALLA,
        default='M',
        verbose_name="Talla"
    )

    # 5. Color del artículo
    color = models.CharField(
        max_length=40,
        verbose_name="Color"
    )

    # 6. Precio: validado estrictamente mayor a 0 ($CLP)
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1.0)],
        verbose_name="Precio ($CLP)"
    )

    # 7. Stock en almacén: valor entero no negativo
    stock = models.PositiveIntegerField(
        default=0,
        verbose_name="Stock disponible"
    )

    # 8. URL de la fotografía de catálogo
    imagen_url = models.URLField(
        max_length=600,
        blank=True,
        verbose_name="URL de Imagen"
    )

    # 9. Descripción y detalles textiles
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción y Material"
    )

    # 10. Estado de disponibilidad
    disponible = models.BooleanField(
        default=True,
        verbose_name="Disponible para venta"
    )

    # 11. Auditoría temporal de creación
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de ingreso"
    )

    class Meta:
        verbose_name = "Prenda"
        verbose_name_plural = "Prendas"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"[{self.categoria}] {self.nombre} (SKU: {self.codigo_sku}) - ${self.precio}"


