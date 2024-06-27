from rest_framework import serializers
from .models import ItemCarrito
from .serializers import ProductoSerializer

class ItemCarritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto', 'cantidad']
