from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet

router = DefaultRouter()
router.register(r'', CategoriaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
