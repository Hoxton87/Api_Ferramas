import pytest
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from productos.models import Categoria
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from rest_framework.test import APIClient

@pytest.mark.django_db
class CategoriaAPITestCase(APITestCase):

    def setUp(self):
        # Crear un usuario de prueba y obtener el token
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')


        # Crear una categoría de prueba
        self.categoria = Categoria.objects.create(nombre='Herramientas')
        self.categorias_url = reverse('categoria-list')
        self.categoria_url = reverse('categoria-detail', args=[self.categoria.id])

    def test_obtener_todas_las_categorias(self):
        response = self.client.get(self.categorias_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_obtener_categoria_por_id(self):
        response = self.client.get(self.categoria_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], self.categoria.nombre)

    def test_crear_categoria_via_api(self):
        data = {'nombre': 'Herramientas Eléctricas'}
        response = self.client.post(self.categorias_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Categoria.objects.count(), 2)  # Verificar que se haya creado una nueva categoría
        self.assertEqual(Categoria.objects.get(id=response.data['id']).nombre, 'Herramientas Eléctricas')

    def test_actualizar_categoria_via_api(self):
        data = {'nombre': 'Herramientas Actualizadas'}
        response = self.client.put(self.categoria_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.categoria.refresh_from_db()
        self.assertEqual(self.categoria.nombre, 'Herramientas Actualizadas')
