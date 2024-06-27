from django.urls import path
from .views import agregar_al_carrito, comprar_productos

urlpatterns = [
    path('agregar/', agregar_al_carrito, name='agregar-al-carrito'),
    path('comprar/', comprar_productos, name='comprar-productos'),
]
