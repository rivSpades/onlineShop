from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from store.models import Product,Variation
from .models import Cart,CartItem
# Create your views here.



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
    
    