from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count

from products.models import Product, Category
# from enquiries.models import Enquiry

# Create your views here.

def dashboard_home(request):
    featured_products = Product.objects.filter(
        is_featured=True,
        is_available=True
    ).select_related('category')[:6]

    if not featured_products:
        featured_products = Product.objects.filter(
            is_available=True
        ).select_related('category')[:6]

    top_categories = Category.objects.annotate(
        total_products=Count('products')
    ).order_by('-total_products')[:4]

    # recent_enquiries = Enquiry.objects.order_by('-created_at')[:5]

    context = {
        'featured_products': featured_products,
        'available_products_count': Product.objects.filter(is_available=True).count(),
        'featured_products_count': Product.objects.filter(is_featured=True, is_available=True).count(),
        # 'new_enquiries_count': Enquiry.objects.filter(status='new').count(),
        # 'recent_enquiries': recent_enquiries,
        'top_categories': top_categories,
    }

    return render(request, 'dashboard/dashboard_home.html', context)
