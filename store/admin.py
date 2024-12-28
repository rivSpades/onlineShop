from django.contrib import admin
from .models import (
    Product,
    Variation,
    ProductImage,
    Brand,
    Gender,
    VariationType,
    Unit
)
from django.utils.html import format_html


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')


# Inline for Product Images
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms displayed by default


# Inline for Variations
class VariationInline(admin.TabularInline):
    model = Variation
    extra = 1  # Number of empty forms displayed by default
    fields = ('variation_type', 'value', 'price', 'unit', 'quantity', 'is_active')
    list_editable = ('is_active',)





@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_date', 'modified_date')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'brand', 'gender', 'get_variations', 'modified_date', 'is_avaliable')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'brand', 'gender', 'is_avaliable')
    search_fields = ('name', 'brand__name', 'category__name', 'gender__name')

    # Define which inlines should appear on the Product form page
    inlines = [
        VariationInline,
    ]

    def get_variations(self, obj):
        """Return a formatted list of variations for the product."""
        variations = obj.variations.all()
        return ", ".join([f"{v.variation_type.name}: {v.value} ({v.quantity} in stock)" for v in variations])
    
    get_variations.short_description = 'Variations'



@admin.register(VariationType)
class VariationTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_date')
    search_fields = ('name',)


# Admin for Variation
@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('variation_type', 'product', 'value', 'price', 'unit', 'quantity', 'is_active', 'get_images')
    list_editable = ('is_active', 'quantity')  # Allow editing quantity directly in the list view
    list_filter = ('variation_type', 'product')
    search_fields = ('product__name', 'variation_type__name', 'value')

    # Method to display images in the variation admin
    def get_images(self, obj):
        """Return HTML to display the images associated with this variation."""
        images = ProductImage.objects.filter(variation=obj)
        if images:
            return format_html('<br/>'.join([f'<img src="{image.image.url}" width="50" height="50" />' for image in images]))
        return "No images"
    
    get_images.short_description = 'Variation Images'



@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')
    search_fields = ('product__name',)
