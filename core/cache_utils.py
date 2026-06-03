"""
Centralized cache key management and caching utilities for Bhavani Cashews.

All cache keys are defined here to prevent key collisions
and enable systematic invalidation.
"""
from functools import wraps
from django.core.cache import cache
import logging

logger = logging.getLogger("bhavani.cache")

# ─── Cache Key Templates ───
CACHE_KEYS = {
    "featured_products": "products:featured",
    "newest_products": "products:newest",
    "all_categories": "categories:active",
    "product_detail": "products:detail:{slug}",
    "product_list": "products:list:sort={sort}&page={page}",
    "category_products": "products:category:{slug}:sort={sort}&page={page}",
    "dashboard_stats": "dashboard:stats",
    "available_count": "products:available_count",
    "featured_count": "products:featured_count",
}

# ─── TTL Constants (seconds) ───
TTL_SHORT = 300       # 5 minutes  — volatile data (counts, dashboard)
TTL_MEDIUM = 900      # 15 minutes — product listings
TTL_LONG = 3600       # 1 hour     — categories, rarely changing data


def invalidate_product_caches():
    """Bulk-invalidate all product-related cache keys."""
    keys_to_delete = [
        CACHE_KEYS["featured_products"],
        CACHE_KEYS["newest_products"],
        CACHE_KEYS["available_count"],
        CACHE_KEYS["featured_count"],
        CACHE_KEYS["dashboard_stats"],
    ]
    cache.delete_many(keys_to_delete)
    # Pattern-based deletion for paginated/detail keys
    try:
        from django_redis import get_redis_connection
        conn = get_redis_connection("default")
        for pattern in ("*products:list:*", "*products:category:*", "*products:detail:*"):
            cursor = 0
            while True:
                cursor, keys = conn.scan(cursor, match=pattern, count=100)
                if keys:
                    conn.delete(*keys)
                if cursor == 0:
                    break
        logger.info("Product caches invalidated successfully (pattern scan)")
    except Exception as exc:
        logger.warning("Pattern-based cache invalidation failed (%s), clearing all", exc)
        cache.clear()  # Nuclear fallback


def invalidate_category_caches():
    """Invalidate category-related cache keys."""
    cache.delete(CACHE_KEYS["all_categories"])
    logger.info("Category caches invalidated successfully")
