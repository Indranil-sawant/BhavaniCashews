from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Order, OrderStatus

@receiver(pre_save, sender=Order)
def restore_stock_on_cancel(sender, instance, **kwargs):
    """
    If an order's status is changed to CANCELLED, restore stock for all of its items.
    """
    if not instance.pk:
        return
        
    try:
        old_instance = Order.objects.get(pk=instance.pk)
    except Order.DoesNotExist:
        return
        
    # Check if status has changed to CANCELLED
    if old_instance.status != OrderStatus.CANCELLED and instance.status == OrderStatus.CANCELLED:
        from django.db.models import F
        # Use single-query update with F expressions by referencing product_id directly.
        # This completely avoids N+1 database queries to fetch each product model.
        for item in instance.items.all():
            Product.objects.filter(pk=item.product_id).update(stock=F('stock') + item.quantity)
