from rest_framework.test import APITestCase
from django.urls import reverse
from productos.models import Producto
from categorias.models import Categoria
from carrito.models import Carrito
from items_carrito.models import ItemCarrito
from django.contrib.auth.models import User

class AgregarAlCarritoTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.producto = Producto.objects.create(
            nombre='Laptop',
            descripcion='Una laptop de prueba',
            precio=1000.00,
            modelo='Model X',
            marca='Brand Y',
            codigo='12345',
            stock=10,
            categoria=self.categoria
        )
        self.client.login(username='testuser', password='password')

    def test_agregar_producto_al_carrito(self):
        url = reverse('agregar-al-carrito')
        data = {'producto_id': self.producto.id, 'cantidad': 2}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Carrito.objects.first().items.first().producto.nombre, 'Laptop')


class CarritoDetalleTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.producto = Producto.objects.create(
            nombre='Laptop',
            descripcion='Una laptop de prueba',
            precio=1000.00,
            modelo='Model X',
            marca='Brand Y',
            codigo='12345',
            stock=10,
            categoria=self.categoria
        )
        self.carrito = Carrito.objects.create(user=self.user)
        self.item_carrito = ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        self.client.login(username='testuser', password='password')

    def test_carrito_detalle(self):
        url = reverse('carrito-detalle')
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['items'][0]['producto']['nombre'], 'Laptop')
        self.assertEqual(response.data['items'][0]['cantidad'], 2)


class ComprarProductosTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.producto = Producto.objects.create(
            nombre='Laptop',
            descripcion='Una laptop de prueba',
            precio=1000.00,
            modelo='Model X',
            marca='Brand Y',
            codigo='12345',
            stock=10,
            categoria=self.categoria
        )
        self.carrito = Carrito.objects.create(user=self.user)
        self.item_carrito = ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        self.client.login(username='testuser', password='password')

    def test_comprar_productos(self):
        url = reverse('comprar-productos')
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['message'], 'Compra realizada con éxito')
        self.assertFalse(Carrito.objects.filter(user=self.user).exists())
        self.assertEqual(Producto.objects.get(id=self.producto.id).stock, 8)


class AgregarProductoSinStockTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.categoria = Categoria.objects.create(nombre='Electrónica')
        self.producto = Producto.objects.create(
            nombre='Laptop',
            descripcion='Una laptop de prueba',
            precio=1000.00,
            modelo='Model X',
            marca='Brand Y',
            codigo='12345',
            stock=1,
            categoria=self.categoria
        )
        self.client.login(username='testuser', password='password')

    def test_agregar_producto_sin_stock(self):
        url = reverse('agregar-al-carrito')
        data = {'producto_id': self.producto.id, 'cantidad': 2}
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data['error'], 'Stock insuficiente para el producto')
