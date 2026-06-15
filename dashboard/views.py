from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.core.cache import cache

from products.models import Product, Category
from core.cache_utils import CACHE_KEYS, TTL_SHORT
# from enquiries.models import Enquiry


def dashboard_home(request):
    # ─── Dashboard stats (cached) ───
    dashboard_data = cache.get(CACHE_KEYS["dashboard_stats"])

    if dashboard_data is None:
        featured_products = list(
            Product.objects.filter(
                is_featured=True,
                is_available=True
            ).select_related('category')[:6]
        )

        if not featured_products:
            featured_products = list(
                Product.objects.filter(
                    is_available=True
                ).select_related('category')[:6]
            )

        top_categories = list(
            Category.objects.annotate(
                total_products=Count('products')
            ).order_by('-total_products')[:6]
        )

        available_products_count = Product.objects.filter(is_available=True).count()
        featured_products_count = Product.objects.filter(
            is_featured=True, is_available=True
        ).count()

        dashboard_data = {
            'featured_products': featured_products,
            'available_products_count': available_products_count,
            'featured_products_count': featured_products_count,
            'top_categories': top_categories,
        }

        cache.set(CACHE_KEYS["dashboard_stats"], dashboard_data, TTL_SHORT)

    # recent_enquiries = Enquiry.objects.order_by('-created_at')[:5]
    # dashboard_data['new_enquiries_count'] = Enquiry.objects.filter(status='new').count()
    # dashboard_data['recent_enquiries'] = recent_enquiries

    return render(request, 'dashboard/dashboard_home.html', dashboard_data)
