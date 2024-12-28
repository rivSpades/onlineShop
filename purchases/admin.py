from django.contrib import admin
from .models import Supplier, PaymentPurchase, Purchase, PurchaseProduct

class PurchaseProductInline(admin.TabularInline):
    model = PurchaseProduct
    extra = 0  # Allows adding purchase products from the Purchase Admin page

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_number', 'supplier', 'status', 'total_amount', 'order_date','stock_updated']
    inlines = [PurchaseProductInline]
    readonly_fields = ['purchase_number','total_amount','stock_updated']  # Make the purchase_number read-only in the admin interface
    
    def calculated_total_amount(self, obj):
        return obj.calculated_total_amount
    
    calculated_total_amount.short_description = 'Total Amount'  # Customize the label in the admin panel
    
    def save_model(self, request, obj, form, change):
        # Ensure that total amount is recalculated before saving the purchase
        obj.save()  # This will trigger the `save` method in the model, including recalculating total_amount
        super().save_model(request, obj, form, change)

admin.site.register(Supplier)
admin.site.register(PaymentPurchase)
admin.site.register(Purchase, PurchaseAdmin)
