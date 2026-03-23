from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import CartItem
from store.models import Product

def get_cart_items(request):
    if request.user.is_authenticated:
        return CartItem.objects.filter(user=request.user)
    elif request.session.session_key:
        return CartItem.objects.filter(session_key=request.session.session_key)
    return CartItem.objects.none()

def cart_view(request):
    cart_items = get_cart_items(request)
    cart_total = sum(item.get_total() for item in cart_items)
    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    if request.method == 'POST':
        size = request.POST.get('size', 'M')
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > product.stock:
            messages.error(request, 'Not enough stock available.')
            return redirect('product_detail', slug=product.slug)
        
        if request.user.is_authenticated:
            cart_item, created = CartItem.objects.get_or_create(
                user=request.user,
                product=product,
                size=size,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        else:
            if not request.session.session_key:
                request.session.save()
            cart_item, created = CartItem.objects.get_or_create(
                session_key=request.session.session_key,
                product=product,
                size=size,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
        
        messages.success(request, f'{product.name} added to cart!')
        return redirect('cart_view')
    
    return redirect('product_detail', slug=product.slug)

def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        
        if request.user.is_authenticated:
            if cart_item.user != request.user:
                return redirect('cart_view')
        else:
            if cart_item.session_key != request.session.session_key:
                return redirect('cart_view')
        
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0 and quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated.')
        else:
            messages.error(request, 'Invalid quantity.')
    
    return redirect('cart_view')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.user.is_authenticated:
        if cart_item.user == request.user:
            cart_item.delete()
    elif request.session.session_key:
        if cart_item.session_key == request.session.session_key:
            cart_item.delete()
    
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_view')
