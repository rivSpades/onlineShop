from django.contrib import admin
from .models import Payment,Order,OrderProduct
# Register your models here.


class orderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields =('payment','user','product','quantity','product_price','is_ordered','variation')
    extra = 0 #remove extra blank lines

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number','first_name','last_name','phone','email','country','city','order_total','status','created_at']
    list_filter=['status','is_ordered']
    search_fields=['order_number','first_name','last_name','email','phone']
    list_per_page = 20
    inlines = [orderProductInline]



admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)                    