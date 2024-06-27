from django.urls import path
from .views import CarritoDetailView

urlpatterns = [
    path('', CarritoDetailView.as_view(), name='carrito-detalle'),
]
