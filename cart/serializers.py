from rest_framework import serializers
from .models import CartItem
from store.models import ProductImage
from store.serializers import VariationSerializer, ProductImageSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.name')
    price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2)
    variation = serializers.SerializerMethodField()  # Custom method to serialize variations
    images = serializers.SerializerMethodField()  # Custom method to serialize product images

    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_name', 'quantity', 'price', 'variation', 'is_active', 'images']

    def get_variation(self, obj):
        """Serialize variations linked to the cart item."""
        variations = obj.variation.all()  # Assuming 'variation' is a ManyToMany field
        return VariationSerializer(variations, many=True, context=self.context).data

    def get_images(self, obj):
        """Fetch images associated with the product or its variations."""
        product_images = obj.product.product_images.all()
        variation_images = ProductImage.objects.filter(variation__in=obj.variation.all())
        images = product_images | variation_images  # Combine product and variation images
        return ProductImageSerializer(images, many=True, context=self.context).data
