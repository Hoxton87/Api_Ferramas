from rest_framework import viewsets
from .models import MovimientoInventario
from .serializers import MovimientoInventarioSerializer

class MovimientoInventarioViewSet(viewsets.ModelViewSet):
    queryset = MovimientoInventario.objects.all()
    serializer_class = MovimientoInventarioSerializer
