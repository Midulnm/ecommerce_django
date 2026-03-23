from django.shortcuts import get_object_or_404
from cart.models import CartItem

def cart(request):
    cart_items = []
    cart_total = 0
    cart_items_count = 0
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    elif request.session.session_key:
        cart_items = CartItem.objects.filter(session_key=request.session.session_key)
    
    for item in cart_items:
        cart_total += item.product.price * item.quantity
        cart_items_count += item.quantity
    
    return {
        'cart_items': cart_items,
        'cart_total': cart_total,
        'cart_items_count': cart_items_count,
    }
