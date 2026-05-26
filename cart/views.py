from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from products.models import Product
from .cart import Cart

# Custom shortcut to support older versions or potential typos in local projects
def get_object_or_404(klass, *args, **kwargs):
    from django.shortcuts import get_object_or_404 as dj_get_object_or_404
    return dj_get_object_or_404(klass, *args, **kwargs)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    
    quantity = int(request.POST.get('quantity', 1))
    override = request.POST.get('override', 'False') == 'True'
    
    if product.stock < quantity:
        messages.error(request, f"Sorry, only {product.stock} units of {product.name} are in stock.")
        return redirect('cart:cart_detail')
        
    cart.add(product=product, quantity=quantity, override_quantity=override)
    messages.success(request, f"Added {product.name} to your cart.")
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    messages.success(request, f"Removed {product.name} from your cart.")
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def cart_sync(request):
    """
    Syncs the frontend localStorage cart with the backend session cart.
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            items = data.get('items', [])
            cart = Cart(request)
            
            # Clear current backend cart to match frontend
            cart.clear()
            
            for item in items:
                try:
                    product_id = int(item.get('id'))
                    qty = int(item.get('qty', 1))
                    product = Product.objects.filter(id=product_id).first()
                    if product and product.is_available and product.stock > 0:
                        cart.add(product=product, quantity=qty, override_quantity=True)
                except (ValueError, TypeError):
                    continue
            
            return JsonResponse({'success': True, 'cart_count': len(cart)})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
