from .models import Product,Variation
from django.contrib import admin




class ProductAdmin(admin.ModelAdmin):
    list_display=('name','price','stock','category','modified_date','created_date','is_avaliable')
    prepopulated_fields={'slug':('name',)}


class VariationAdmin(admin.ModelAdmin):
    list_display=('name','product','value','is_active')
    list_editable=('is_active',)
    list_filter = ('name','product','value',)

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
