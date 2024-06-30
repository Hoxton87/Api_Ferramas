from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from productos.models import Producto, Carrito, Categoria

class AgregarAlCarritoIntegrationTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        # Creación de una categoría para pruebas
        self.categoria = Categoria.objects.create(nombre='Herramientas')

        # Creación de un producto asociado a la categoría
        self.producto = Producto.objects.create(
            nombre='Producto de Prueba',
            precio=100,
            stock=10,
            categoria=self.categoria
        )

    def test_agregar_producto_al_carrito_api(self):
        url = '/api/agregar_al_carrito/'
        data = {
            'producto_id': self.producto.id,
            'cantidad': 2
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que el producto se agregó al carrito correctamente
        carrito = Carrito.objects.get(user=self.user)
        self.assertTrue(carrito.items.filter(producto=self.producto).exists())

    def test_compra_exitosa(self):
        # Agrega productos al carrito
        self.client.post('/api/agregar_al_carrito/', {'producto_id': self.producto.id, 'cantidad': 2}, format='json')

        url = '/api/comprar_productos/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verifica que el carrito esté vacío después de la compra
        carrito = Carrito.objects.filter(user=self.user).first()
        self.assertIsNone(carrito)

    def test_stock_insuficiente(self):
        self.producto.stock = 0
        self.producto.save()

        url = '/api/agregar_al_carrito/'
        data = {
            'producto_id': self.producto.id,
            'cantidad': 1
        }

        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_carrito_vacio(self):
        url = '/api/comprar_productos/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
