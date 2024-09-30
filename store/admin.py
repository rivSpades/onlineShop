from .models import Product
from django.contrib import admin




class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','stock','category','modified_date','created_date','is_avaliable')
    prepopulated_fields={'slug':('name',)}


admin.site.register(Product,ProductAdmin)
