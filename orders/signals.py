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
        for item in instance.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
