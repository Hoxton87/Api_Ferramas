# productos/views.py
from rest_framework import viewsets, generics, status
from .models import Categoria, Producto, ItemCarrito, Carrito
from .serializers import CategoriaSerializer, ProductoSerializer, CarritoSerializer, ItemCarritoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import transaction

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer

@api_view(['POST'])
def agregar_al_carrito(request):
    user = request.user
    producto_id = request.data.get('producto_id')
    cantidad = request.data.get('cantidad', 1)

    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return Response({'error': 'Producto no encontrado'}, status=status.HTTP_404_NOT_FOUND)

    if producto.stock < int(cantidad):
        return Response({'error': 'Stock insuficiente para el producto'}, status=status.HTTP_400_BAD_REQUEST)

    carrito, created = Carrito.objects.get_or_create(user=user, defaults={'created_at': timezone.now()})

    item_carrito, created = ItemCarrito.objects.get_or_create(carrito=carrito, producto=producto, defaults={'cantidad': cantidad})

    if not created:
        item_carrito.cantidad += int(cantidad)
        item_carrito.save()

    return Response({'message': 'Producto agregado al carrito'}, status=status.HTTP_200_OK)


class CarritoDetailView(generics.RetrieveAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def get_object(self):
        return Carrito.objects.get(user=self.request.user)

@api_view(['POST'])
@transaction.atomic
def comprar_productos(request):
    user = request.user
    carrito = Carrito.objects.get(user=user)
    if not carrito.items.exists():
        return Response({'error': 'El carrito está vacío'}, status=status.HTTP_400_BAD_REQUEST)
    
    total = 0
    for item in carrito.items.all():
        if item.producto.stock < item.cantidad:
            return Response({'error': f'Stock insuficiente para el producto {item.producto.nombre}'}, status=status.HTTP_400_BAD_REQUEST)
        total += item.producto.precio * item.cantidad
    
    for item in carrito.items.all():
        item.producto.stock -= item.cantidad
        item.producto.save()
    
    carrito.items.all().delete()
    carrito.delete()
    
    return Response({'message': 'Compra realizada con éxito', 'total': total}, status=status.HTTP_200_OK)
