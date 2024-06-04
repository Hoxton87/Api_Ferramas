# productos/management/commands/load_productos.py
import json
import os
from django.core.management.base import BaseCommand
from productos.models import Categoria, Producto

class Command(BaseCommand):
    help = 'Cargar categorías y productos desde un archivo JSON'

    def handle(self, *args, **kwargs):
        json_file_path = os.path.join(os.path.dirname(__file__), '../../productos.json')
        with open(json_file_path, 'r', encoding='utf-8') as file:  # Especificar la codificación UTF-8
            data = json.load(file)
            for categoria_data in data:
                categoria, created = Categoria.objects.get_or_create(nombre=categoria_data['categoria'])
                for producto_data in categoria_data['productos']:
                    Producto.objects.create(
                        nombre=producto_data['nombre'],
                        descripcion=producto_data['descripcion'],
                        precio=producto_data['precio'],
                        modelo=producto_data['modelo'],
                        marca=producto_data['marca'],
                        codigo=producto_data['codigo'],
                        stock=producto_data['stock'],
                        categoria=categoria
                    )
        self.stdout.write(self.style.SUCCESS('Categorías y productos cargados exitosamente'))
