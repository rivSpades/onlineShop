from .models import Cart,CartItem


def cart_items_count(request):
    cart_item_count = 0

    cart_items = CartItem.objects.all().filter(cart__cart_session_id=Cart._get_cart_id(request))
    if not cart_items:
        return dict(cart_item_count=cart_item_count)
    for cart_item in cart_items:
        cart_item_count += cart_item.quantity

    return dict(cart_item_count=cart_item_count)