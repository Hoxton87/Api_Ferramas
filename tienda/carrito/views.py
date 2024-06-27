from rest_framework import generics
from .models import Carrito
from .serializers import CarritoSerializer

class CarritoDetailView(generics.RetrieveAPIView):
    queryset = Carrito.objects.all()
    serializer_class = CarritoSerializer

    def get_object(self):
        return Carrito.objects.get(user=self.request.user)
