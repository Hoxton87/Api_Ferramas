from rest_framework import serializers
from .models import Carrito
from items_carrito.serializers import ItemCarritoSerializer

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)
    class Meta:
        model = Carrito
        fields = ['id', 'user', 'created_at', 'items']
