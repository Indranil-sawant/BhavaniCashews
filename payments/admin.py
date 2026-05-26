from django.contrib import admin
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.utils import timezone
from .models import Payment, PaymentScreenshot
from orders.models import OrderStatus, PaymentStatus

class PaymentScreenshotInline(admin.StackedInline):
    model = PaymentScreenshot
    extra = 0
    readonly_fields = ['screenshot_preview']

    def screenshot_preview(self, obj):
        if obj.screenshot:
            return mark_safe(f'<a href="{obj.screenshot.url}" target="_blank"><img src="{obj.screenshot.url}" style="max-width: 300px; max-height: 300px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);" /></a>')
        return "No image uploaded yet."
    screenshot_preview.short_description = "Screenshot Preview"

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'order_link', 'amount', 'payment_method', 'status', 
        'transaction_id', 'screenshot_status', 'created_at'
    ]
    list_filter = ['payment_method', 'status', 'created_at']
    search_fields = ['id', 'order__id', 'transaction_id']
    inlines = [PaymentScreenshotInline]
    actions = ['approve_payments', 'reject_payments']

    def order_link(self, obj):
        url = reverse('admin:orders_order_change', args=[obj.order.id])
        return mark_safe(f'<a href="{url}" style="font-weight: bold; color: #10b981;">Order #{str(obj.order.id)[:8]}</a>')
    order_link.short_description = "Order"

    def screenshot_status(self, obj):
        if hasattr(obj, 'screenshot'):
            if obj.screenshot.is_verified:
                return mark_safe('<span style="background-color: #d1fae5; color: #065f46; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Verified</span>')
            return mark_safe('<span style="background-color: #fef3c7; color: #92400e; padding: 3px 10px; border-radius: 12px; font-size: 11px; font-weight: bold;">Pending Review</span>')
        return "No Screenshot"
    screenshot_status.short_description = "Screenshot Status"

    def approve_payments(self, request, queryset):
        for payment in queryset:
            payment.status = PaymentStatus.PAID
            payment.save()
            
            # Update screenshot verification
            if hasattr(payment, 'screenshot'):
                screenshot = payment.screenshot
                screenshot.is_verified = True
                screenshot.verified_at = timezone.now()
                screenshot.verified_by = request.user
                screenshot.save()
                
            # Update order
            order = payment.order
            order.payment_status = PaymentStatus.PAID
            order.status = OrderStatus.CONFIRMED
            order.save()
            
        self.message_user(request, f"Successfully approved {queryset.count()} payments.")
    approve_payments.short_description = "Approve selected payments & orders"

    def reject_payments(self, request, queryset):
        for payment in queryset:
            payment.status = PaymentStatus.FAILED
            payment.save()
            
            # Update screenshot
            if hasattr(payment, 'screenshot'):
                screenshot = payment.screenshot
                screenshot.is_verified = False
                screenshot.rejection_reason = "Rejected via admin actions."
                screenshot.save()
                
            # Update order
            order = payment.order
            order.payment_status = PaymentStatus.FAILED
            order.save()
            
        self.message_user(request, f"Successfully rejected {queryset.count()} payments.")
    reject_payments.short_description = "Reject selected payments & orders"
