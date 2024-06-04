# productos/serializers.py
from rest_framework import serializers
from .models import Categoria, Producto

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(slug_field='nombre', queryset=Categoria.objects.all())

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'modelo', 'marca', 'codigo', 'stock', 'categoria']
