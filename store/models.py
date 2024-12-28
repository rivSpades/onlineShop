from django.db import models

from category.models import Category
from django.urls import reverse


class Brand(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Gender(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "Men", "Women", "Unisex"
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.FloatField()
    long_description = models.TextField(max_length=500, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True) 
    gender = models.ForeignKey(Gender, on_delete=models.CASCADE,null=True)  # One gender per product
    is_avaliable = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    @property
    def stock(self):
        # Aggregate stock from all active variations
        return sum(variation.quantity for variation in self.variations.filter(is_active=True))

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.category.slug, self.slug])

    def __str__(self):
        return self.name





class Unit(models.Model):
    name = models.CharField(max_length=50, unique=True)  # e.g., "kg", "m", "liter"
    symbol = models.CharField(max_length=10, unique=True)  # e.g., "kg", "m", "L"

    def __str__(self):
        return self.name

class VariationType(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "color", "size"
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Variation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    variation_type = models.ForeignKey(VariationType, related_name='variations', on_delete=models.CASCADE, null=True)
    value = models.CharField(max_length=100)
    quantity = models.IntegerField(default=0)  # Stock for this specific variation
    unit = models.ForeignKey(Unit, related_name='variations', on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)  # Price specific to the variation
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.unit:
            return f"{self.variation_type.name}: {self.value} ({self.unit.symbol})"
        return f"{self.variation_type.name}: {self.value}"

    @property
    def effective_price(self):
        """Return the price of the variation, falling back to the product price if not set."""
        return self.price if self.price is not None else self.product.price



class ProductImage(models.Model):
    variation = models.ForeignKey(Variation, related_name='images', on_delete=models.CASCADE, null=True, blank=True)  # Link image to variation
    product = models.ForeignKey(Product, related_name='product_images', on_delete=models.CASCADE, null=True, blank=True)  # Optionally, keep a link to product in case it's needed
    image = models.ImageField(upload_to='photos/products')

    def __str__(self):
        # If linked to a variation, display variation details in the string representation
        if self.variation:
            return f"{self.variation.product.name} - {self.variation.variation_type.name}: {self.variation.value} Image"
        # Otherwise, use product name if no variation
        return f"{self.product.name} Image"