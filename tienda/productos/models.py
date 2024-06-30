from django.db import models
from categorias.models import Categoria

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    modelo = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    codigo = models.CharField(max_length=100)
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, related_name='productos', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
