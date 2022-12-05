from rest_framework import serializers

from .models import *

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['product_id', 'name', 'description', 'price', 'main_image']

