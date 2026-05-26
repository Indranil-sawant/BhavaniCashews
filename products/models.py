from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CashewGrade(models.Model):
    GRADE_CHOICES = (
        ('W180', 'W180'),
        ('W210', 'W210'),
        ('W240', 'W240'),
        ('W320', 'W320'),
        ('W400', 'W400'),
        ('Splits', 'Splits'),
        ('JK', 'JK'),
        ('K', 'K'),
        ('LWP', 'LWP'),
        ('SWP', 'SWP'),
        ('SP', 'SP'),
        ('SW', 'SW'),
        ('Kani', 'Kani'),
        ('NW', 'NW'),
    )

    name = models.CharField(
        max_length=20,
        choices=GRADE_CHOICES,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    image = models.ImageField(
        upload_to='cashew_grades/',
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    grade = models.ForeignKey(
        CashewGrade,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )

    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.TextField()
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    minimum_order_quantity = models.PositiveIntegerField(default=1)
    image = models.ImageField(upload_to='products/')
    secondary_image = models.ImageField(upload_to='products/', blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    sku = models.CharField(max_length=50, unique=True, null=True, blank=True)
    weight = models.DecimalField(
        max_digits=6, 
        decimal_places=2, 
        default=0.00,
        help_text="Weight in grams"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    PACKAGING_CHOICES = (
            ('250g', '250g'),
            ('500g', '500g'),
            ('1kg', '1kg'),
            ('5kg', '5kg'),
            ('10kg', '10kg'),
            )

    packaging_size = models.CharField(
            max_length=20,
            choices=PACKAGING_CHOICES,
            default='1kg'
            )

    origin = models.CharField(
            max_length=100,
            blank=True,
            null=True,
            help_text="Origin location of cashews"
            )

    is_export_quality = models.BooleanField(default=False)

    discount_price = models.DecimalField(
            max_digits=10,
            decimal_places=2,
            blank=True,
            null=True
            )

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductGallery(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery'
    )
    image = models.ImageField(upload_to='products/gallery/')

    class Meta:
        verbose_name_plural = 'Product Galleries'

    def __str__(self):
        return f"Gallery Image for {self.product.name}"


class ProductReview(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    name = models.CharField(max_length=255)
    rating = models.PositiveIntegerField(
        choices=[(i, i) for i in range(1, 6)]
    )
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Review by {self.name} for {self.product.name} ({self.rating}★)"