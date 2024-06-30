from django.test import TestCase
from productos.models import Categoria

class CategoriaModelTest(TestCase):

    def setUp(self):
        self.categoria = Categoria.objects.create(nombre="Herramientas Manuales")

    def test_crear_categoria_con_nombre(self):
        Categoria.objects.create(nombre="Herramientas")
        categoria = Categoria.objects.get(nombre="Herramientas")
        self.assertEqual(categoria.nombre, "Herramientas")

    def test_str_categoria(self):
        self.assertEqual(str(self.categoria), "Herramientas Manuales")

    def test_crear_categoria_sin_nombre(self):
        with self.assertRaises(Exception):
            Categoria.objects.create(nombre=None)

    def test_editar_categoria(self):
        self.categoria.nombre = "Herramientas y Equipos"
        self.categoria.save()
        self.assertEqual(self.categoria.nombre, "Herramientas y Equipos")
