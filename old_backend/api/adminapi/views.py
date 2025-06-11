# backend/api/views.py
from rest_framework import generics
from .serializers import *
from rest_framework.viewsets import ModelViewSet
from .models import Products


class ProductsViewSet(ModelViewSet):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer

