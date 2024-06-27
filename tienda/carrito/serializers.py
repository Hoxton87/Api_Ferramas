from rest_framework import serializers
from .models import Carrito

class CarritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrito
        fields = ['id', 'user', 'created_at']
