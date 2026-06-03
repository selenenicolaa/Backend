from django.urls import path
from .views import inicio, productos

urlpatterns = [
    path('', inicio),
    path('api/productos', productos),
]