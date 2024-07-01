import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from productos.models import Producto
from carrito.models import Carrito
from categorias.models import Categoria
from items_carrito.models import ItemCarrito
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
class AgregarAlCarritoTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.categoria = Categoria.objects.create(nombre='Herramientas')
        self.producto = Producto.objects.create(
            nombre='Producto de Prueba',
            precio=100,
            stock=10,
            categoria=self.categoria
        )

    def test_agregar_producto_al_carrito(self):
        url = '/api/agregar_al_carrito/'
        data = {
            'producto_id': self.producto.id,
            'cantidad': 2
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        carrito = Carrito.objects.get(user=self.user)
        self.assertTrue(carrito.items.filter(producto=self.producto).exists())

    def test_producto_no_encontrado(self):
        url = '/api/agregar_al_carrito/'
        data = {
            'producto_id': 999,  # ID de producto inexistente
            'cantidad': 1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_actualizar_item_carrito(self):
        url = '/api/agregar_al_carrito/'
        data = {
            'producto_id': self.producto.id,
            'cantidad': 2
        }

        self.client.post(url, data, format='json')

        data['cantidad'] = 3
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        item_carrito = ItemCarrito.objects.get(carrito__user=self.user, producto=self.producto)
        self.assertEqual(item_carrito.cantidad, 3)

    def test_vaciar_carrito(self):
        url = '/api/vaciar_carrito/'
        self.client.post('/api/agregar_al_carrito/', {'producto_id': self.producto.id, 'cantidad': 2}, format='json')

        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        carrito = Carrito.objects.get(user=self.user)
        self.assertFalse(carrito.items.exists())
