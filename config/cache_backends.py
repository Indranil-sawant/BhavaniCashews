"""
Enterprise fault-tolerant Redis cache backend for Bhavani Cashews.

Wraps django_redis.cache.RedisCache and intercepts ConnectionError,
TimeoutError, and redis.exceptions.* to gracefully degrade to
LocMemCache. Prevents 500 errors during Redis outages.
"""
import logging
from functools import wraps

from django.core.cache.backends.locmem import LocMemCache
from django_redis.cache import RedisCache
from redis.exceptions import ConnectionError, TimeoutError, RedisError

logger = logging.getLogger("bhavani.cache")

_fallback_cache = LocMemCache("fallback-cache", {})


def _graceful(method_name):
    """Decorator that catches Redis errors and falls back to LocMemCache."""
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            try:
                return func(self, *args, **kwargs)
            except (ConnectionError, TimeoutError, RedisError, OSError) as exc:
                logger.error(
                    "Redis %s failed (%s: %s) — falling back to LocMemCache",
                    method_name, type(exc).__name__, exc,
                )
                fallback_method = getattr(_fallback_cache, method_name)
                return fallback_method(*args, **kwargs)
        return wrapper
    return decorator


class FallbackRedisCache(RedisCache):
    """Redis cache with automatic LocMemCache fallback on connection failure."""

    @_graceful("get")
    def get(self, key, default=None, version=None):
        return super().get(key, default=default, version=version)

    @_graceful("set")
    def set(self, key, value, timeout=None, version=None):
        return super().set(key, value, timeout=timeout, version=version)

    @_graceful("delete")
    def delete(self, key, version=None):
        return super().delete(key, version=version)

    @_graceful("get_many")
    def get_many(self, keys, version=None):
        return super().get_many(keys, version=version)

    @_graceful("set_many")
    def set_many(self, mapping, timeout=None, version=None):
        return super().set_many(mapping, timeout=timeout, version=version)

    @_graceful("delete_many")
    def delete_many(self, keys, version=None):
        return super().delete_many(keys, version=version)

    @_graceful("has_key")
    def has_key(self, key, version=None):
        return super().has_key(key, version=version)

    @_graceful("clear")
    def clear(self):
        return super().clear()

    @_graceful("incr")
    def incr(self, key, delta=1, version=None):
        return super().incr(key, delta=delta, version=version)
