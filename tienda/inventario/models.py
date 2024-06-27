from django.db import models
from productos.models import Producto

class MovimientoInventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    tipo_movimiento = models.CharField(max_length=50, choices=[('Entrada', 'Entrada'), ('Salida', 'Salida')])
    cantidad = models.IntegerField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.tipo_movimiento} - {self.producto.nombre}'
