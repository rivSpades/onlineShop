# serializers.py
from rest_framework import serializers
from .models import CartItem
from store.serializers import VariationSerializer,ProductImageSerializer



class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    variation = VariationSerializer(many=True, read_only=True)  # Nested serializer for variations
    images = ProductImageSerializer(source='product.images', many=True)  # Include product images

    class Meta:
        model = CartItem
        fields = ['id','product_id', 'product_name', 'quantity', 'price', 'variation', 'is_active','images']
