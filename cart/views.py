from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from store.models import Product,Variation
from django.http import JsonResponse
from .models import Cart,CartItem
from .serializers import CartItemSerializer
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class AddCartView(View):
         

    def post(self,request,product_id):

        product = get_object_or_404(Product,id=product_id )
        product_variation=[]
      

        #in case of a product with more than 1 variation need to do a for to handle that
        for item in request.POST:
        
            key=item
            value=request.POST[key]
            try:
             
                variation = Variation.objects.get( name__iexact=key ,value__iexact=value , product=product)
             
            except:
                continue                
            
            product_variation.append(variation)
        


  
        cart, created = Cart.objects.get_or_create(cart_session_id=Cart._get_cart_id(request))
        
        cart_item  = CartItem.objects.filter(product=product, cart=cart)
        
        #it will append all the combinations of variations in every cart item
       
        print(cart_item)
        variation_found=False

        if cart_item:
            for item in cart_item:
                existing_variations=[]
                
                existing_variations.append(list(item.variation.all()))

            #will go check if there is a item with the same combination of variations (a cart item can have more than 1 variation). if yes will increase the quantity
                if product_variation in existing_variations:
                    item.quantity +=1
                    item.save()  
                    variation_found=True
                    break
                    


                           
                
        if not cart_item or not variation_found:
            new_cart_item  = CartItem.objects.create(product=product, cart=cart,quantity=1)
            if (product_variation):
                
                new_cart_item.variation.set(product_variation)
        
                new_cart_item.save()
        

        return redirect('cart:cart')   
    

class RemoveCartView(View):
         

    def get(self,request,product_id,cart_item_id):
      
        remove_item = request.GET.get('remove_item', 'False') == 'True'
        cart = Cart.objects.get(cart_session_id=Cart._get_cart_id(request))
        product = get_object_or_404(Product,id=product_id)
        cart_item = get_object_or_404(CartItem, product=product, cart=cart , id=cart_item_id)


        if cart_item.quantity > 1 and not remove_item :
            cart_item.quantity -= 1
            cart_item.save()
        elif cart_item.quantity <1 or remove_item:
            cart_item.delete()

        return redirect('cart:cart')       

class CartView(View):
    def get(self,request,total=0,quantity=0,cart_items=None):
        tax=0
        grand_total=0
        cart=Cart.objects.get(cart_session_id=Cart._get_cart_id(request))
        print(cart)
        cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        print(cart_items)
        if not cart_items:
            pass
        for cart_item in cart_items:
            total=total + (cart_item.product.price * cart_item.quantity)
         

    
        tax=0.02*total
        grand_total=total+tax
        context={
            "total":total,
            "tax":tax,
            "grand_total":grand_total,
            "cart_items":cart_items,
        }
        return render(request,'store/cart.html',context)
    


class ApiCartView(APIView):
    def get(self, request):
        try:
            # Retrieve or create the cart using session ID
            cart = Cart.objects.get(cart_session_id=Cart._get_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

            # Calculate total, tax, and grand total
            total = sum(item.product.price * item.quantity for item in cart_items)
            tax = 0.02 * total
            grand_total = total + tax

            # Serialize the cart items
            cart_items_data = CartItemSerializer(cart_items, many=True).data

            # Construct the response data
            cart_data = {
                'total': total,
                'tax': tax,
                'grand_total': grand_total,
                'cart_items': cart_items_data,
            }

            return Response(cart_data, status=status.HTTP_200_OK)

        except Cart.DoesNotExist:
            return Response({"error": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        

class ApiAddCartView(APIView):
    def post(self, request, product_id):
        # Fetch the product by ID
        product = get_object_or_404(Product, id=product_id)
        product_variations = []

        # Parse the variations and quantity from request data
        variations_data = request.data.get('variations', {})
        quantity = request.data.get('quantity', 1)  # Default to 1 if not provided

        for key, value in variations_data.items():
            try:
                # Find the specific variation for the product
                variation = Variation.objects.get(name__iexact=key, value__iexact=value, product=product)
                product_variations.append(variation)
            except Variation.DoesNotExist:
                continue

        # Get or create a cart for the current session
        cart, created = Cart.objects.get_or_create(cart_session_id=Cart._get_cart_id(request))

        # Check if this product with these specific variations already exists in the cart
        cart_item_qs = CartItem.objects.filter(product=product, cart=cart)
        variation_found = False

        if cart_item_qs.exists():
            for item in cart_item_qs:
                # Get variations associated with this cart item
                existing_variations = list(item.variation.all())

                # Check if the existing cart item has the same set of variations
                if set(product_variations) == set(existing_variations):
                    # If so, update the quantity
                    item.quantity += quantity  # Update by specified quantity
                    item.save()
                    variation_found = True
                    break

        # If no cart item with the same variations exists, create a new cart item
        if not variation_found:
            new_cart_item = CartItem.objects.create(
                product=product,
                cart=cart,
                quantity=quantity,  # Set quantity based on request
                is_active=True
            )
            if product_variations:
                new_cart_item.variation.set(product_variations)
            new_cart_item.save()

        return Response({"message": "Product added to cart successfully"}, status=status.HTTP_201_CREATED)


    
    