import pytest
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.urls import reverse
from productos.models import Producto
from carrito.models import Carrito
from categorias.models import Categoria
from items_carrito.models import ItemCarrito

@pytest.mark.django_db
class ComprarProductosIntegrationTestCase(APITestCase):

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

    def test_compra_exitosa_con_stock_suficiente(self):
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)

        url = reverse('comprar-productos')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Compra realizada con éxito')
        self.assertEqual(response.data['total'], 200)

        # Verificar que el carrito se elimina después de la compra
        carrito = Carrito.objects.filter(user=self.user).first()
        self.assertIsNone(carrito)

    def test_comprar_productos_con_stock_insuficiente(self):
        self.producto.stock = 1
        self.producto.save()
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)

        url = reverse('comprar-productos')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

        # Verificar que el carrito aún existe y los ítems no se eliminaron
        carrito = Carrito.objects.filter(user=self.user).first()
        self.assertIsNotNone(carrito)
        self.assertTrue(carrito.items.exists())

    def test_comprar_productos_con_carrito_vacio(self):
        url = reverse('comprar-productos')
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_vaciar_carrito_despues_de_compra_exitosa(self):
        ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)

        # Realizar la compra
        url_compra = reverse('comprar-productos')
        response_compra = self.client.post(url_compra)
        self.assertEqual(response_compra.status_code, status.HTTP_200_OK)

        # Verificar que el carrito se vacíe correctamente
        url_vaciar_carrito = reverse('vaciar-carrito')
        response_vaciar = self.client.post(url_vaciar_carrito)
        self.assertEqual(response_vaciar.status_code, status.HTTP_200_OK)

        carrito = Carrito.objects.filter(user=self.user).first()
        self.assertIsNone(carrito)
