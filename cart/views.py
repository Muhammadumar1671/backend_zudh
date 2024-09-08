from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .models import Cart, CartItem
from shop.models import Product  # Assuming your product model is in the 'shop' app

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = None

    # Get or create a cart for the current user or session
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        cart_id = request.session.get('cart_id')
        if cart_id:
            cart = Cart.objects.filter(id=cart_id).first()
        if not cart:
            cart = Cart.objects.create()
            request.session['cart_id'] = cart.id

    # Add item to cart or update quantity
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
    cart_item.save()

    return JsonResponse({'status': 'success', 'message': 'Product added to cart'})




def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if cart_item.cart.user == request.user or cart_item.cart.id == request.session.get('cart_id'):
        cart_item.delete()
        return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid operation'}, status=403)




def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    quantity = request.POST.get('quantity')

    if cart_item.cart.user == request.user or cart_item.cart.id == request.session.get('cart_id'):
        try:
            quantity = int(quantity)
            if quantity > 0:
                cart_item.quantity = quantity
                cart_item.save()
            else:
                cart_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Cart updated successfully'})
        except ValueError:
            return JsonResponse({'status': 'error', 'message': 'Invalid quantity'}, status=400)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid operation'}, status=403)


