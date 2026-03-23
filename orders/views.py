from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Order, OrderItem
from cart.models import CartItem
from cart.views import get_cart_items

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/order_history.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def checkout(request):
    cart_items = get_cart_items(request)
    
    if not cart_items.exists():
        messages.error(request, 'Your cart is empty.')
        return redirect('cart_view')
    
    cart_total = sum(item.get_total() for item in cart_items)
    
    return render(request, 'orders/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

@login_required
def place_order(request):
    if request.method == 'POST':
        cart_items = get_cart_items(request)
        
        if not cart_items.exists():
            messages.error(request, 'Your cart is empty.')
            return redirect('cart_view')
        
        full_name = request.POST.get('full_name')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        
        cart_total = sum(item.get_total() for item in cart_items)
        
        order = Order.objects.create(
            user=request.user,
            full_name=full_name,
            address=address,
            phone=phone,
            total_amount=cart_total
        )
        
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                size=item.size,
                quantity=item.quantity,
                price=item.product.price
            )
            
            item.product.stock -= item.quantity
            item.product.save()
        
        cart_items.delete()
        
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('order_detail', order_id=order.id)
    
    return redirect('checkout')
