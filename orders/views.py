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
        
    # Lock the products in the database using select_for_update() to prevent race conditions
    from django.db.models import F
    product_ids = [item['product'].id for item in cart]
    locked_products = {p.id: p for p in Product.objects.select_for_update().filter(id__in=product_ids)}
    
    # Verify stock status under write-lock
    for item in cart:
        product = locked_products.get(item['product'].id)
        if not product or product.stock < item['quantity']:
            messages.error(request, f"Product '{item['product'].name}' is out of stock or does not have enough quantity ({product.stock if product else 0} left).")
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
        # Deduct stock safely under atomic lock using database F-expressions
        product = locked_products.get(item['product'].id)
        product.stock = F('stock') - item['quantity']
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
    orders = Order.objects.filter(user=request.user).prefetch_related('items', 'items__product', 'shipping_address')
    return render(request, 'orders/order_list.html', {'orders': orders})

import json
import uuid
from django.http import JsonResponse
from products.models import Product

@login_required
@transaction.atomic
def b2b_inquiry(request):
    """
    Creates a B2B Wholesale / Export order entry in the database from custom quote submissions.
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
        
    try:
        # Support both form data and json POST submissions
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        company_name = data.get('company_name', '').strip()
        contact_name = data.get('contact_name', '').strip()
        business_email = data.get('business_email', '').strip()
        cashew_grade = data.get('cashew_grade', '').strip()
        estimated_volume = data.get('estimated_volume', '').strip()
        inquiry_message = data.get('inquiry_message', '').strip()
        
        if not contact_name or not business_email or not cashew_grade:
            return JsonResponse({'success': False, 'error': 'Missing required B2B fields'}, status=400)
            
        # 1. Create B2B Order
        order = Order.objects.create(
            user=request.user,
            payment_method=PaymentMethod.B2B,
            payment_status=PaymentStatus.PENDING,
            status=OrderStatus.PLACED,
            subtotal=Decimal('0.00'),
            taxes=Decimal('0.00'),
            shipping=Decimal('0.00'),
            cod_charge=Decimal('0.00'),
            total=Decimal('0.00'),
            transaction_id=f"B2B-{uuid.uuid4().hex[:8].upper()}"
        )
        
        # 2. Create ShippingAddress holding company and specifications
        ShippingAddress.objects.create(
            order=order,
            full_name=contact_name,
            email=business_email,
            phone="B2B Request",
            address_line1=company_name if company_name else "Individual Inquiry",
            address_line2=f"Grade: {cashew_grade} | Est. Volume: {estimated_volume}",
            city="B2B Export Division",
            state=inquiry_message[:100] if inquiry_message else "Custom B2B Quotation Request",
            postal_code="000000",
            country="India"
        )
        
        # 3. Match Product to add OrderItem representation
        # Try to find a matching product by grade name
        product = Product.objects.filter(name__icontains=cashew_grade).first()
        if not product:
            # Fallback to flagship if no match
            product = Product.objects.filter(is_featured=True).first() or Product.objects.first()
            
        if product:
            OrderItem.objects.create(
                order=order,
                product=product,
                price=Decimal('0.00'),
                quantity=1
            )
            
        return JsonResponse({
            'success': True, 
            'order_id': str(order.id),
            'order_number': order.transaction_id
        })
        
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
