import uuid
from django.db import models
from django.conf import settings
from products.models import Product

class OrderStatus(models.TextChoices):
    PLACED = 'PLACED', 'Placed'
    CONFIRMED = 'CONFIRMED', 'Confirmed'
    SHIPPED = 'SHIPPED', 'Shipped'
    DELIVERED = 'DELIVERED', 'Delivered'
    CANCELLED = 'CANCELLED', 'Cancelled'

class PaymentMethod(models.TextChoices):
    UPI = 'UPI', 'UPI ID/Intent'
    QR = 'QR', 'QR Code Scanner'
    COD = 'COD', 'Cash On Delivery'
    B2B = 'B2B', 'B2B Wholesale / Export'

class PaymentStatus(models.TextChoices):
    PENDING = 'PENDING', 'Pending'
    PROCESSING = 'PROCESSING', 'Processing'
    PAID = 'PAID', 'Paid'
    FAILED = 'FAILED', 'Failed'
    REFUNDED = 'REFUNDED', 'Refunded'

class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PLACED
    )
    payment_method = models.CharField(
        max_length=20,
        choices=PaymentMethod.choices
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING
    )
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    taxes = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    shipping = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cod_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    transaction_id = models.CharField(max_length=100, blank=True, null=True, unique=True)
    qr_code = models.ImageField(upload_to='payment_qr/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} (Order {self.order.id})"

    @property
    def get_cost(self):
        return self.price * self.quantity


class ShippingAddress(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping_address')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100, default='India')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Shipping Address for Order {self.order.id}"
