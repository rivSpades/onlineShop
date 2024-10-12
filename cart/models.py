from django.db import models
from store.models import Product,Variation


class Cart(models.Model):
    cart_session_id = models.CharField(max_length=250,blank=True)
    created_date=models.DateField(auto_now_add=True)

    def _get_cart_id(request):
        cart_id = request.session.session_key
        if not cart_id:
            cart_id = request.session.create()
        return cart_id   

    def __str__(self):
        return self.cart_session_id
    

class CartItem(models.Model):
    product = models.ForeignKey(Product ,on_delete=models.CASCADE)
    variation = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return self.product.name