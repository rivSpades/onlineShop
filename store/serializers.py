from rest_framework import serializers
from .models import Product,Variation,ProductImage
from category.models import Category,MainCategory

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'slug', 'description', 'image']

class CategorySerializer(serializers.ModelSerializer):
    main_category = MainCategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'main_category']

class VariationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variation
        fields = ['id', 'name', 'value', 'is_active']  # Customize the fields as needed        

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']  # You can include any other fields you may need

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    variations = VariationSerializer(many=True, read_only=True)  # Include variations
    images = ProductImageSerializer(many=True, read_only=True)  # Nested serializer for images

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'images', 'stock',
            'is_avaliable', 'category', 'created_date', 'modified_date','variations'
        ]


