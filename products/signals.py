"""
Cache invalidation signals for the products app.

Automatically clears relevant Redis cache keys when Product
or Category objects are created, updated, or deleted.
"""
import logging
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import Product, Category
from core.cache_utils import invalidate_product_caches, invalidate_category_caches

logger = logging.getLogger("bhavani.cache")


@receiver(post_save, sender=Product)
@receiver(post_delete, sender=Product)
def on_product_change(sender, instance, **kwargs):
    """Invalidate product caches when any product is saved or deleted."""
    logger.info("Product '%s' changed — invalidating product caches", instance.name)
    invalidate_product_caches()


@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def on_category_change(sender, instance, **kwargs):
    """Invalidate category caches when any category is saved or deleted."""
    logger.info("Category '%s' changed — invalidating category caches", instance.name)
    invalidate_category_caches()
    invalidate_product_caches()  # Categories affect product listings too
