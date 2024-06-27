# proyecto/urls.py

from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/categorias/', include('categorias.urls')),
    path('api/', include('productos.urls')),
    path('api/carrito/', include('carrito.urls')),
    path('api/items_carrito/', include('items_carrito.urls')),
    path('api/clientes/', include('clientes.urls')),
    path('api/pedidos/', include('pedidos.urls')),
    path('api/proveedores/', include('proveedores.urls')),
    path('api/inventarios/', include('inventario.urls')),
]
