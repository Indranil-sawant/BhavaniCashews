from django.contrib import admin
from .models import Order, OrderItem, ShippingAddress

class ShippingAddressInline(admin.StackedInline):
    model = ShippingAddress
    can_delete = False
    verbose_name_plural = 'Shipping Address'

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'payment_method', 'payment_status', 'status',
        'subtotal', 'taxes', 'shipping', 'cod_charge', 'total', 'created_at'
    ]
    list_filter = ['payment_method', 'payment_status', 'status', 'created_at']
    search_fields = ['id', 'user__username', 'transaction_id']
    inlines = [ShippingAddressInline, OrderItemInline]
    readonly_fields = ['qr_code']
    list_editable = ['payment_status', 'status']
    ordering = ['-created_at']
