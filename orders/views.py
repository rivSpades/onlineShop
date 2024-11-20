from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly,AllowAny,IsAuthenticated  # Allows unauthenticated access for some parts
from rest_framework_simplejwt.authentication import JWTAuthentication  # ass
from rest_framework.pagination import PageNumberPagination
from django.utils.crypto import get_random_string
from cart.models import CartItem
from .models import Order, OrderProduct, Payment
from .utils import send_order_email
from .serializers import OrderSerializer  # Make sure to create this serializer if you want to return order details

class ApiPlaceOrder(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Extract cart items for the authenticated user
        cart_items = CartItem.objects.filter(user=request.user)
        paypal_order_data = request.data.get("order")
        print(paypal_order_data)
        if not paypal_order_data:
            return Response({"error": "No payment details"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not cart_items.exists():
            return Response({"error": "Your cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Extract order and payment information from request data
    


        # Calculate order total and tax
        order_total = sum(item.product.price * item.quantity for item in cart_items)
        tax = order_total * 0.1  # Assume a 10% tax rate
        grand_total=order_total+tax

        payment = Payment.objects.create(
            user=request.user,
            payment_id=paypal_order_data.get("id"),
            payment_method="PayPal",
            amount_paid=grand_total,
            status=paypal_order_data.get("status"),
            
        )
        # Step 2: Create Order record
        order = Order.objects.create(
            user=request.user,
            payment=payment,
            first_name=request.data.get("first_name"),
            last_name=request.data.get("last_name"),
            phone=request.data.get("phone"),
            email=request.data.get("email"),
            address_line_1=request.data.get("address_line_1"),
            address_line_2=request.data.get("address_line_2",""),
            country=request.data.get("country"),
            state=request.data.get("state"),
            city=request.data.get("city"),
            order_note=request.data.get("order_note", ""),
            order_total=grand_total,
            tax=tax,
            ip=request.META.get("REMOTE_ADDR"),
            
        )


       
        order.order_number=  Order._generate_order_number(order)

        if paypal_order_data.get("status") =="COMPLETED":
            order.is_ordered=True

        order.save()


        for item in cart_items:
            order_product = OrderProduct.objects.create(
                order=order,
                payment = payment,
                user = request.user,
                product = item.product,
                quantity = item.quantity,
                product_price = item.product.price,
                is_ordered=True

            )

            product_variation = item.variation.all()
            order_product.variation.set(product_variation)

            item.product.stock -= item.quantity
            item.product.save()
      
        order_product.save()

        send_order_email(request.user,order)

        cart_items.delete()

        order_serializer = OrderSerializer(order)

        return Response(
            {
                "message": "Order placed successfully!",
                "order": order_serializer.data
            },
            status=status.HTTP_201_CREATED
        )

class ApiOrderDetail(APIView):
  
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, order_number):
        token = request.META.get('HTTP_AUTHORIZATION', " ").split(' ')[1]
        print(token)
        print(request.user)
        print(request.user.is_authenticated)
        try:
            # Retrieve the order based on the order number and user
           
            order = Order.objects.get(order_number=order_number,user=request.user )

            # Serialize the order data
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found or you do not have access to it."},
                status=status.HTTP_404_NOT_FOUND
            )
        
class ApiOrderView(ListAPIView):
    """
    API to list all orders for the authenticated user.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        # Return orders for the logged-in user
        return Order.objects.filter(user=self.request.user).order_by('-created_at')