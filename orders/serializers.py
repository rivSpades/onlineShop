from rest_framework import serializers
from .models import Order, OrderProduct,Payment
from store.serializers import ProductImageSerializer

class OrderProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(source='product.images', many=True)  # Include product images
    product_id = serializers.IntegerField(source='product.id')
    product_name = serializers.CharField(source='product.name')
    class Meta:
        model = OrderProduct
        fields = ['product_id', 'product_name', 'variation', 'quantity', 'product_price','images']



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['payment_id', 'payment_method', 'amount_paid', 'status', 'created_at']


class OrderSerializer(serializers.ModelSerializer):
    ordered_products = OrderProductSerializer(many=True, source='orderproduct_set', read_only=True)
    payment_details = PaymentSerializer(source='payment', read_only=True)  # Nested Payment Serializer
    class Meta:
        model = Order
        fields = [
            'order_number', 'first_name', 'last_name', 'phone', 'email', 'address_line_1',
            'address_line_2', 'country', 'state', 'city', 'order_note', 'order_total', 'tax',
            'status', 'ordered_products','payment_details'
        ]
