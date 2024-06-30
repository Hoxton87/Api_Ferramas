from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from productos.models import Producto, Carrito, ItemCarrito, Categoria

class ComprarProductosTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

        self.categoria = Categoria.objects.create(nombre='Herramientas')
        self.producto = Producto.objects.create(
            nombre='Producto de Prueba',
            precio=100,
            stock=10,
            categoria=self.categoria
        )
        self.carrito = Carrito.objects.create(user=self.user)

    def test_comprar_productos_con_stock_suficiente(self):
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)

        url = '/api/comprar_productos/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Compra realizada con éxito')
        self.assertEqual(response.data['total'], 200)

    def test_comprar_productos_con_stock_insuficiente(self):
        self.producto.stock = 1
        self.producto.save()
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)

        url = '/api/comprar_productos/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_comprar_productos_carrito_vacio(self):
        url = '/api/comprar_productos/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_comprar_productos_elimina_items_del_carrito(self):
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)

        url = '/api/comprar_productos/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        carrito = Carrito.objects.filter(user=self.user).first()
        self.assertIsNone(carrito)
