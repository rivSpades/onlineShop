# serializers.py
from rest_framework import serializers
from .models import MainCategory, Category

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)  # Reference the new related name

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'subcategories']  # Include subcategories

class MainCategorySerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = MainCategory
        fields = ['id', 'name', 'slug', 'description', 'image', 'categories']
