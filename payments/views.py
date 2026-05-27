from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from decimal import Decimal

from orders.models import Order, PaymentMethod, PaymentStatus, OrderStatus
from .models import Payment, PaymentScreenshot
from .utils import generate_upi_link, generate_qr_code, verify_payment_reference

@login_required
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Ensure it's a UPI/QR order
    if order.payment_method not in [PaymentMethod.UPI, PaymentMethod.QR]:
        messages.error(request, "This order does not require online payment.")
        return redirect('orders:order_detail', order_id=order.id)
        
    upi_id = getattr(settings, 'MERCHANT_UPI_ID', 'merchant@upi')
    merchant_name = getattr(settings, 'MERCHANT_NAME', 'Bhavani Cashews')
    
    # Generate UPI URI Link
    upi_link = generate_upi_link(
        upi_id=upi_id,
        merchant_name=merchant_name,
        amount=order.total,
        order_id=order.id
    )
    
    # Generate QR Code image dynamically if not already generated
    if not order.qr_code:
        qr_file = generate_qr_code(upi_link)
        order.qr_code.save(f"order_{order.id}_qr.png", qr_file, save=True)
        
    context = {
        'order': order,
        'upi_id': upi_id,
        'merchant_name': merchant_name,
        'upi_link': upi_link,
    }
    return render(request, 'payments/upi_payment.html', context)

@login_required
@require_POST
def upload_payment_screenshot(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    transaction_id = request.POST.get('transaction_id', '').strip()
    screenshot_file = request.FILES.get('screenshot')
    
    if not verify_payment_reference(transaction_id):
        messages.error(request, "Please enter a valid Transaction Reference ID (minimum 6 characters).")
        return redirect('payments:payment_page', order_id=order.id)
        
    if not screenshot_file:
        messages.error(request, "Please upload your payment confirmation screenshot.")
        return redirect('payments:payment_page', order_id=order.id)
        
    # Enforce size limits (Max 5MB)
    max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5242880)
    if screenshot_file.size > max_size:
        messages.error(request, f"The uploaded file size exceeds the maximum limit of {max_size // 1048576}MB.")
        return redirect('payments:payment_page', order_id=order.id)

    # Validate true image integrity using Pillow
    from PIL import Image
    try:
        # Open and verify file is a valid image
        img = Image.open(screenshot_file)
        img.verify()
        
        # Verify it is PNG or JPEG
        if img.format not in ['JPEG', 'PNG']:
            messages.error(request, "Invalid file format. Only JPG, JPEG and PNG images are accepted.")
            return redirect('payments:payment_page', order_id=order.id)
            
        # Reset file pointer after verify() / reading
        screenshot_file.seek(0)
    except Exception:
        messages.error(request, "Uploaded file is corrupted or not a valid image.")
        return redirect('payments:payment_page', order_id=order.id)

    # Obfuscate filename to prevent directory traversals and conflicts
    import os
    import uuid
    ext = os.path.splitext(screenshot_file.name)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        ext = '.jpg' if img.format == 'JPEG' else '.png'
    screenshot_file.name = f"receipt_{uuid.uuid4().hex}{ext}"
        
    # Check if a payment for this order already exists
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'amount': order.total,
            'payment_method': order.payment_method,
            'status': PaymentStatus.PROCESSING,
            'transaction_id': transaction_id
        }
    )
    
    if not created:
        payment.transaction_id = transaction_id
        payment.status = PaymentStatus.PROCESSING
        payment.save()
        
    # Create or update screenshot
    PaymentScreenshot.objects.update_or_create(
        payment=payment,
        defaults={
            'screenshot': screenshot_file,
            'is_verified': False
        }
    )
    
    # Update Order info
    order.transaction_id = transaction_id
    order.payment_status = PaymentStatus.PROCESSING
    order.save()
    
    messages.success(request, "Payment screenshot uploaded successfully! Our team is verifying your payment.")
    return redirect('orders:order_success', order_id=order.id)

@login_required
def cod_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_method != PaymentMethod.COD:
        messages.error(request, "This order is not configured for Cash On Delivery.")
        return redirect('orders:order_detail', order_id=order.id)
        
    # Create COD Payment entry if not exists
    Payment.objects.get_or_create(
        order=order,
        defaults={
            'amount': order.total,
            'payment_method': PaymentMethod.COD,
            'status': PaymentStatus.PENDING
        }
    )
    
    messages.success(request, "Order placed successfully using Cash On Delivery!")
    return redirect('orders:order_success', order_id=order.id)

@login_required
@user_passes_test(lambda u: u.is_staff)
def verify_payment(request, payment_id):
    """
    Staff-only view to verify transaction screenshot and mark payment and order as completed.
    """
    payment = get_object_or_404(Payment, id=payment_id)
    screenshot = getattr(payment, 'screenshot', None)
    
    if not screenshot:
        messages.error(request, "No screenshot found for this payment.")
        return redirect('admin:payments_payment_changelist')
        
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            # Update Payment
            payment.status = PaymentStatus.PAID
            payment.save()
            
            # Update Screenshot
            screenshot.is_verified = True
            screenshot.verified_at = timezone.now()
            screenshot.verified_by = request.user
            screenshot.save()
            
            # Update Order
            order = payment.order
            order.payment_status = PaymentStatus.PAID
            order.status = OrderStatus.CONFIRMED
            order.save()
            
            messages.success(request, f"Payment for Order {order.id} approved successfully!")
        elif action == 'reject':
            reason = request.POST.get('reason', 'Invalid details or missing screenshot.')
            # Update Payment
            payment.status = PaymentStatus.FAILED
            payment.save()
            
            # Update Screenshot
            screenshot.is_verified = False
            screenshot.rejection_reason = reason
            screenshot.save()
            
            # Update Order
            order = payment.order
            order.payment_status = PaymentStatus.FAILED
            order.save()
            
            messages.warning(request, f"Payment for Order {order.id} rejected. Reason: {reason}")
            
    return redirect('admin:payments_payment_changelist')
