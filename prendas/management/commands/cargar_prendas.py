"""
COMANDO PERSONALIZADO DE DJANGO:
Ruta: prendas/management/commands/cargar_prendas.py
Ejecución: python manage.py cargar_prendas
Descripción:
    Puebla la tabla 'prendas_prenda' en la base de datos MariaDB (XAMPP)
    con 10 registros iniciales: 5 Poleras y 5 Hoodies.
"""

from django.core.management.base import BaseCommand
from prendas.models import Prenda

class Command(BaseCommand):
    help = 'Carga 10 prendas iniciales en la base de datos (5 Poleras y 5 Hoodies)'

    def handle(self, *args, **kwargs):
        articulos = [
            # 5 POLERAS
            {
                'nombre': 'Polera Heavyweight Boxy Fit',
                'codigo_sku': 'POL-001',
                'categoria': Prenda.CATEGORIA_POLERA,
                'talla': 'L',
                'color': 'Negro Lavado',
                'precio': 19990.00,
                'stock': 25,
                'imagen_url': 'https://images.unsplash.com/photo-1521572267360-ee0c2909d518?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Algodon peinado premium de 240 GSM con corte rectangular moderno.',
                'disponible': True
            },
            {
                'nombre': 'Polera Minimalist Studio White',
                'codigo_sku': 'POL-002',
                'categoria': Prenda.CATEGORIA_POLERA,
                'talla': 'M',
                'color': 'Blanco Puro',
                'precio': 15990.00,
                'stock': 30,
                'imagen_url': 'https://images.unsplash.com/photo-1581655353564-df123a1eb820?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Polera regular fit de textura ligera y cuello redondo acanalado.',
                'disponible': True
            },
            {
                'nombre': 'Polera Graphic Typography Atelier',
                'codigo_sku': 'POL-003',
                'categoria': Prenda.CATEGORIA_POLERA,
                'talla': 'XL',
                'color': 'Gris Pizarra',
                'precio': 22990.00,
                'stock': 12,
                'imagen_url': 'https://images.unsplash.com/photo-1503342217505-b0a15ec3261c?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Estampa tipografica minimalista en serigrafia tacto suave.',
                'disponible': True
            },
            {
                'nombre': 'Polera Raw Edge Vintage Olive',
                'codigo_sku': 'POL-004',
                'categoria': Prenda.CATEGORIA_POLERA,
                'talla': 'S',
                'color': 'Verde Militar',
                'precio': 18990.00,
                'stock': 18,
                'imagen_url': 'https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Terminaciones al corte en mangas y cuello con teñido artesanal.',
                'disponible': True
            },
            {
                'nombre': 'Polera Ribbed Texture Sand',
                'codigo_sku': 'POL-005',
                'categoria': Prenda.CATEGORIA_POLERA,
                'talla': 'M',
                'color': 'Arena Beige',
                'precio': 17990.00,
                'stock': 20,
                'imagen_url': 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Punto acanalado flexible con calce relajado de media estacion.',
                'disponible': True
            },

            # 5 HOODIES
            {
                'nombre': 'Hoodie French Terry Heavyweight',
                'codigo_sku': 'HOD-001',
                'categoria': Prenda.CATEGORIA_HOODIE,
                'talla': 'L',
                'color': 'Gris Jaspeado',
                'precio': 42990.00,
                'stock': 15,
                'imagen_url': 'https://images.unsplash.com/photo-1556905055-8f358a7a47b2?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Felpa francesa de 450 GSM con capucha sin cordones estructurada.',
                'disponible': True
            },
            {
                'nombre': 'Hoodie Full Zip Boxy Core',
                'codigo_sku': 'HOD-002',
                'categoria': Prenda.CATEGORIA_HOODIE,
                'talla': 'M',
                'color': 'Negro Carbon',
                'precio': 45990.00,
                'stock': 10,
                'imagen_url': 'https://images.unsplash.com/photo-1509967419530-da38b4704bc6?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Cierre metalico frontal doble via con corte ancho contemporaneo.',
                'disponible': True
            },
            {
                'nombre': 'Hoodie Washed Mocha Limited',
                'codigo_sku': 'HOD-003',
                'categoria': Prenda.CATEGORIA_HOODIE,
                'talla': 'XL',
                'color': 'Cafe Mocha',
                'precio': 47990.00,
                'stock': 8,
                'imagen_url': 'https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Teñido en prenda pigmentado con bolsillos laterales discretos.',
                'disponible': True
            },
            {
                'nombre': 'Hoodie Relaxed Fleece Bone',
                'codigo_sku': 'HOD-004',
                'categoria': Prenda.CATEGORIA_HOODIE,
                'talla': 'S',
                'color': 'Blanco Hueso',
                'precio': 39990.00,
                'stock': 14,
                'imagen_url': 'https://images.unsplash.com/photo-1578587018452-892bacefd3f2?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Interior perchado suave de alta retencion termica con puños gruesos.',
                'disponible': True
            },
            {
                'nombre': 'Hoodie Drop Shoulder Midnight',
                'codigo_sku': 'HOD-005',
                'categoria': Prenda.CATEGORIA_HOODIE,
                'talla': 'L',
                'color': 'Azul Marino',
                'precio': 44990.00,
                'stock': 9,
                'imagen_url': 'https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=700&auto=format&fit=crop&q=80',
                'descripcion': 'Caida de hombro pronunciada con silueta holgada sin costura central.',
                'disponible': True
            }
        ]

        for item in articulos:
            prenda, creada = Prenda.objects.update_or_create(
                codigo_sku=item['codigo_sku'],
                defaults=item
            )
            if creada:
                self.stdout.write(self.style.SUCCESS(f"[OK] Creada: {prenda.nombre} ({prenda.codigo_sku})"))
            else:
                self.stdout.write(self.style.WARNING(f"[ACTUALIZADA] {prenda.nombre} ({prenda.codigo_sku})"))