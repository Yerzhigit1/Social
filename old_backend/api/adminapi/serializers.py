# backend/api/serializers.py
from rest_framework import serializers
from .models import Products


class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'
        # read_only_fields = ['']
        
    
    # def validate(self, attrs):
    #     return super().validate(attrs)
    