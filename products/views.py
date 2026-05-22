from django.shortcuts import render, get_object_or_404

from .models import Product


def home(request):

    featured_products = Product.objects.filter(
        is_featured=True,
        is_available=True
    )[:8]

    context = {
        'featured_products': featured_products
    }

    return render(
        request,
        'products/home.html',
        context
    )


def product_list(request):

    products = Product.objects.filter(
        is_available=True
    )

    context = {
        'products': products
    }

    return render(
        request,
        'products/product_list.html',
        context
    )


def product_detail(request, slug):

    product = get_object_or_404(
        Product,
        slug=slug,
        is_available=True
    )

    context = {
        'product': product
    }

    return render(
        request,
        'products/product_detail.html',
        context
    )