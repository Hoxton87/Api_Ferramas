# productos/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, ProductoViewSet, agregar_al_carrito, CarritoDetailView, comprar_productos

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('carrito/agregar/', agregar_al_carrito, name='agregar-al-carrito'),
    path('carrito/', CarritoDetailView.as_view(), name='carrito-detalle'),
    path('carrito/comprar/', comprar_productos, name='comprar-productos'),
]
