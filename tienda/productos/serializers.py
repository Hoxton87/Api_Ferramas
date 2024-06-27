from rest_framework import serializers
from .models import Producto,Categoria

class ProductoSerializer(serializers.ModelSerializer):
    categoria = serializers.SlugRelatedField(slug_field='nombre', queryset=Categoria.objects.all())

    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'descripcion', 'precio', 'modelo', 'marca', 'codigo', 'stock', 'categoria']
