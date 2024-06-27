from django.db import models
from django.contrib.auth.models import User

class Carrito(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
