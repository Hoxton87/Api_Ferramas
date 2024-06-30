import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'tienda.settings'
import django
django.setup()
from django.test import TestCase
from productos.models import Categoria
from django.urls import reverse
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class CategoriaModelTest(TestCase):

    def setUp(self):
        # Crear un usuario de prueba
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # Crear una categoría de prueba
        self.categoria = Categoria.objects.create(nombre='Herramientas')
        self.categorias_url = reverse('categoria-list')
        self.categoria_url = reverse('categoria-detail', args=[self.categoria.id])

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
