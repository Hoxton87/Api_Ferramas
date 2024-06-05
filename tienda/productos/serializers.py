# productos/serializers.py
from rest_framework import serializers
from .models import Categoria, Producto, Carrito, ItemCarrito

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(slug_field='nombre', queryset=Categoria.objects.all())

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'modelo', 'marca', 'codigo', 'stock', 'categoria']

class ItemCarritoSerializer(serializers.ModelSerializer):
    producto = ProductoSerializer(read_only=True)

    class Meta:
        model = ItemCarrito
        fields = ['id', 'producto', 'cantidad']

class CarritoSerializer(serializers.ModelSerializer):
    items = ItemCarritoSerializer(many=True, read_only=True)

    class Meta:
        model = Carrito
        fields = ['id', 'user', 'created_at', 'items']
