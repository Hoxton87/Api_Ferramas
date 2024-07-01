import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from productos.models import Producto
from carrito.models import Carrito
from categorias.models import Categoria
from items_carrito.models import ItemCarrito
from django.urls import reverse
from rest_framework.authtoken.models import Token

@pytest.mark.django_db
class AgregarAlCarritoIntegrationTestCase(TestCase):
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
        self.carrito = Carrito.objects.create(user=self.user)

    def test_agregar_producto_al_carrito_api(self):
        url = reverse('agregar-al-carrito')
        data = {'producto_id': self.producto.id, 'cantidad': 2}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_carrito_vacio(self):
        url = reverse('comprar-productos')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_compra_exitosa(self):
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        url = reverse('comprar-productos')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_stock_insuficiente(self):
        self.producto.stock = 1
        self.producto.save()
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        url = reverse('comprar-productos')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)