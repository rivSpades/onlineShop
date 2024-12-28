from rest_framework import serializers
from .models import (
    Product,
    Variation,
    ProductImage,
    Brand,
    Gender,
    Unit,
    VariationType,
    
)
from category.models import Category, MainCategory


class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'slug', 'description', 'image']


class CategorySerializer(serializers.ModelSerializer):
    main_category = MainCategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'main_category']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'slug', 'description', 'created_date', 'modified_date']


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name', 'created_date']

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = ['id', 'name', 'symbol']  # Include both name and symbol if needed


class ProductImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()  # Full URL for the image

    class Meta:
        model = ProductImage
        fields = ['id', 'image_url']

    def get_image_url(self, obj):
        """Build the full URL for the image field."""
        request = self.context.get('request')  # Ensure the request is available
        if obj.image and request:
            return request.build_absolute_uri(obj.image.url)
        return None

class VariationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariationType
        fields = ['id', 'name', 'created_date']


class VariationSerializer(serializers.ModelSerializer):
    variation_type = VariationTypeSerializer(read_only=True)
    unit = UnitSerializer(read_only=True)
    images = serializers.SerializerMethodField()  # Include variation-specific images

    class Meta:
        model = Variation
        fields = ['id', 'variation_type', 'value', 'price', 'unit', 'quantity', 'is_active', 'created_date', 'images']

    def get_images(self, obj):
        """Return all images associated with this variation."""
        images = ProductImage.objects.filter(variation=obj)
        return ProductImageSerializer(images, many=True, context=self.context).data


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    gender = GenderSerializer(read_only=True)
    variations = serializers.SerializerMethodField()
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'long_description',
            'brand', 'gender', 'images', 'stock', 'is_avaliable', 'category',
            'created_date', 'modified_date', 'variations'
        ]

    def get_images(self, obj):
        """Fetch product-level images only (excluding variation images)."""
        product_images = ProductImage.objects.filter(product=obj, variation__isnull=True)
        return ProductImageSerializer(product_images, many=True, context=self.context).data

    def get_variations(self, obj):
        """Fetch all variations for the product, including their images."""
        return VariationSerializer(obj.variations.all(), many=True, context=self.context).data



