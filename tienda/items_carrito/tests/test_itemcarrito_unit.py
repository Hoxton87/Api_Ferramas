from django.test import TestCase
from productos.models import Producto
from categorias.models import Categoria
from carrito.models import Carrito
from items_carrito.models import ItemCarrito
from django.contrib.auth.models import User

class ItemCarritoTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser')
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

    def test_crear_item_carrito(self):
        item_carrito = ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        self.assertEqual(item_carrito.cantidad, 2)
        self.assertEqual(item_carrito.producto.nombre, 'Laptop')
        self.assertEqual(item_carrito.carrito.user.username, 'testuser')

    def test_actualizar_cantidad_item_carrito(self):
        item_carrito = ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        item_carrito.cantidad = 5
        item_carrito.save()
        self.assertEqual(item_carrito.cantidad, 5)

    def test_eliminar_item_carrito(self):
        item_carrito = ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        item_carrito_id = item_carrito.id
        item_carrito.delete()
        with self.assertRaises(ItemCarrito.DoesNotExist):
            ItemCarrito.objects.get(id=item_carrito_id)

    def test_stock_disponible(self):
        item_carrito = ItemCarrito.objects.create(carrito=self.carrito, producto=self.producto, cantidad=2)
        self.assertTrue(self.producto.stock >= item_carrito.cantidad)
