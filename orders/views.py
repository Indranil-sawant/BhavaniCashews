from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.contrib import messages
from django.conf import settings
from decimal import Decimal

from cart.cart import Cart
from .models import Order, OrderItem, ShippingAddress, OrderStatus, PaymentMethod, PaymentStatus
from .forms import CheckoutForm

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty! Add products before checking out.")
        return redirect('cart:cart_detail')
        
    form = CheckoutForm()
    
    # Check if COD is eligible
    cod_max_amount = getattr(settings, 'COD_MAX_AMOUNT', Decimal('5000.00'))
    subtotal = cart.get_subtotal()
    is_cod_eligible = subtotal <= cod_max_amount
    cod_charge = getattr(settings, 'COD_CHARGE', Decimal('50.00'))
    
    context = {
        'cart': cart,
        'form': form,
        'is_cod_eligible': is_cod_eligible,
        'cod_max_amount': cod_max_amount,
        'cod_charge': cod_charge,
    }
    return render(request, 'orders/checkout.html', context)

@login_required
@transaction.atomic
def place_order(request):
    """
    Handles form submission to create order, checks stock, and redirects to payment handler.
    """
    if request.method != 'POST':
        return redirect('orders:checkout')
        
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, "Your cart is empty.")
        return redirect('cart:cart_detail')
        
    form = CheckoutForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Please correct the shipping address errors below.")
        cod_max = getattr(settings, 'COD_MAX_AMOUNT', Decimal('5000.00'))
        return render(request, 'orders/checkout.html', {
            'cart': cart,
            'form': form,
            'is_cod_eligible': cart.get_subtotal() <= cod_max,
            'cod_max_amount': cod_max,
            'cod_charge': getattr(settings, 'COD_CHARGE', Decimal('50.00')),
        })
        
    payment_method = request.POST.get('payment_method')
    if payment_method not in PaymentMethod.values:
        messages.error(request, "Please select a valid payment method.")
        return redirect('orders:checkout')
        
    # Check COD eligibility
    subtotal = cart.get_subtotal()
    cod_max_amount = getattr(settings, 'COD_MAX_AMOUNT', Decimal('5000.00'))
    if payment_method == PaymentMethod.COD and subtotal > cod_max_amount:
        messages.error(request, f"Cash On Delivery is only eligible for orders below ₹{cod_max_amount}.")
        return redirect('orders:checkout')
        
    # Stock pre-check and atomic locking/order creation
    for item in cart:
        product = item['product']
        if product.stock < item['quantity']:
            messages.error(request, f"Product '{product.name}' is out of stock or does not have enough quantity ({product.stock} left).")
            return redirect('cart:cart_detail')
            
    # Calculate costs
    subtotal = cart.get_subtotal()
    taxes = cart.get_tax()
    shipping = cart.get_shipping()
    cod_charge = getattr(settings, 'COD_CHARGE', Decimal('50.00')) if payment_method == PaymentMethod.COD else Decimal('0.00')
    total = subtotal + taxes + shipping + cod_charge
    
    # Create the Order
    order = Order.objects.create(
        user=request.user,
        payment_method=payment_method,
        payment_status=PaymentStatus.PENDING,
        status=OrderStatus.PLACED,
        subtotal=subtotal,
        taxes=taxes,
        shipping=shipping,
        cod_charge=cod_charge,
        total=total
    )
    
    # Create ShippingAddress
    shipping_address = form.save(commit=False)
    shipping_address.order = order
    shipping_address.save()
    
    # Create OrderItems and deduct stock
    for item in cart:
        product = item['product']
        OrderItem.objects.create(
            order=order,
            product=product,
            price=item['price'],
            quantity=item['quantity']
        )
        # Deduct stock safely
        product.stock -= item['quantity']
        product.save()
        
    # Clear the cart on successful database entry
    cart.clear()
    
    # Redirect to corresponding payment step
    if payment_method in [PaymentMethod.UPI, PaymentMethod.QR]:
        return redirect('payments:payment_page', order_id=order.id)
    else:
        # COD direct success
        return redirect('payments:cod_order', order_id=order.id)

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})
