from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.cache import cache
from .models import Category, Product, ProductGallery, ProductReview
from django.contrib.auth.decorators import login_required
from core.cache_utils import CACHE_KEYS, TTL_SHORT, TTL_MEDIUM, TTL_LONG


def home(request):
    # ─── Featured Products (cached) ───
    featured_products = cache.get(CACHE_KEYS["featured_products"])
    if featured_products is None:
        featured_products = list(
            Product.objects.filter(
                is_featured=True,
                is_available=True
            ).select_related('category').only(
                'id', 'name', 'slug', 'short_description', 'price', 'stock',
                'minimum_order_quantity', 'image', 'secondary_image',
                'is_featured', 'created_at', 'category__id', 'category__name'
            )[:6]
        )
        cache.set(CACHE_KEYS["featured_products"], featured_products, TTL_MEDIUM)

    # ─── Newest Products (cached) ───
    newest_products = cache.get(CACHE_KEYS["newest_products"])
    if newest_products is None:
        newest_products = list(
            Product.objects.filter(
                is_available=True
            ).select_related('category').order_by('-created_at').only(
                'id', 'name', 'slug', 'short_description', 'price', 'stock',
                'minimum_order_quantity', 'image', 'secondary_image',
                'is_featured', 'created_at', 'category__id', 'category__name'
            )[:6]
        )
        cache.set(CACHE_KEYS["newest_products"], newest_products, TTL_MEDIUM)

    # ─── Categories (cached) ───
    categories = cache.get(CACHE_KEYS["all_categories"])
    if categories is None:
        categories = list(Category.objects.filter(is_active=True).prefetch_related('products'))
        cache.set(CACHE_KEYS["all_categories"], categories, TTL_LONG)

    # ─── Counts (cached) ───
    available_products_count = cache.get(CACHE_KEYS["available_count"])
    if available_products_count is None:
        available_products_count = Product.objects.filter(is_available=True).count()
        cache.set(CACHE_KEYS["available_count"], available_products_count, TTL_SHORT)

    featured_products_count = cache.get(CACHE_KEYS["featured_count"])
    if featured_products_count is None:
        featured_products_count = Product.objects.filter(is_featured=True, is_available=True).count()
        cache.set(CACHE_KEYS["featured_count"], featured_products_count, TTL_SHORT)

    context = {
        'featured_products': featured_products,
        'newest_products': newest_products,
        'categories': categories,
        'available_products_count': available_products_count,
        'featured_products_count': featured_products_count,
    }

    return render(request, 'products/home.html', context)


def product_list(request):
    current_sort = request.GET.get('sort', 'recommended')
    page = request.GET.get('page', '1')

    # ─── Product list (cached per sort+page) ───
    cache_key = CACHE_KEYS["product_list"].format(sort=current_sort, page=page)
    cached_context = cache.get(cache_key)

    if cached_context is not None:
        return render(request, 'products/product_list.html', cached_context)

    products_list = Product.objects.filter(is_available=True).select_related('category').only(
        'id', 'name', 'slug', 'short_description', 'price', 'stock',
        'minimum_order_quantity', 'image', 'secondary_image',
        'is_featured', 'created_at', 'category__id', 'category__name'
    )

    # ─── Categories (cached) ───
    categories = cache.get(CACHE_KEYS["all_categories"])
    if categories is None:
        categories = list(Category.objects.filter(is_active=True).only('id', 'name', 'slug'))
        cache.set(CACHE_KEYS["all_categories"], categories, TTL_LONG)

    total_products_count = cache.get(CACHE_KEYS["available_count"])
    if total_products_count is None:
        total_products_count = products_list.count()
        cache.set(CACHE_KEYS["available_count"], total_products_count, TTL_SHORT)

    # Sorting
    if current_sort == 'price_asc':
        products_list = products_list.order_by('price')
    elif current_sort == 'price_desc':
        products_list = products_list.order_by('-price')
    elif current_sort == 'newest':
        products_list = products_list.order_by('-created_at')
    else:  # recommended
        products_list = products_list.order_by('-is_featured', '-created_at')

    # Pagination
    paginator = Paginator(products_list, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'total_products_count': total_products_count,
        'current_sort': current_sort,
        'active_category': None,
    }

    cache.set(cache_key, context, TTL_MEDIUM)
    return render(request, 'products/product_list.html', context)


def category_products(request, slug):
    current_sort = request.GET.get('sort', 'recommended')
    page = request.GET.get('page', '1')

    # ─── Category product list (cached per category+sort+page) ───
    cache_key = CACHE_KEYS["category_products"].format(slug=slug, sort=current_sort, page=page)
    cached_context = cache.get(cache_key)

    if cached_context is not None:
        return render(request, 'products/product_list.html', cached_context)

    category = get_object_or_404(Category.objects.only('id', 'slug', 'name', 'is_active'), slug=slug, is_active=True)
    products_list = Product.objects.filter(category=category, is_available=True).select_related('category').only(
        'id', 'name', 'slug', 'short_description', 'price', 'stock',
        'minimum_order_quantity', 'image', 'secondary_image',
        'is_featured', 'created_at', 'category__id', 'category__name'
    )

    # ─── Categories (cached) ───
    categories = cache.get(CACHE_KEYS["all_categories"])
    if categories is None:
        categories = list(Category.objects.filter(is_active=True).only('id', 'name', 'slug'))
        cache.set(CACHE_KEYS["all_categories"], categories, TTL_LONG)

    total_products_count = cache.get(CACHE_KEYS["available_count"])
    if total_products_count is None:
        total_products_count = Product.objects.filter(is_available=True).count()
        cache.set(CACHE_KEYS["available_count"], total_products_count, TTL_SHORT)

    # Sorting
    if current_sort == 'price_asc':
        products_list = products_list.order_by('price')
    elif current_sort == 'price_desc':
        products_list = products_list.order_by('-price')
    elif current_sort == 'newest':
        products_list = products_list.order_by('-created_at')
    else:  # recommended
        products_list = products_list.order_by('-is_featured', '-created_at')

    # Pagination
    paginator = Paginator(products_list, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'total_products_count': total_products_count,
        'current_sort': current_sort,
        'active_category': category,
    }

    cache.set(cache_key, context, TTL_MEDIUM)
    return render(request, 'products/product_list.html', context)


@login_required
def product_detail(request, slug):
    # POST requests (reviews) bypass cache
    if request.method == 'POST':
        product = get_object_or_404(
            Product.objects.select_related('category').prefetch_related('gallery', 'reviews'),
            slug=slug,
            is_available=True
        )
        name = request.POST.get('name')
        rating = request.POST.get('rating')
        review_text = request.POST.get('review')

        if name and rating and review_text:
            ProductReview.objects.create(
                product=product,
                name=name,
                rating=int(rating),
                review=review_text
            )
            # Invalidate this product's detail cache
            detail_cache_key = CACHE_KEYS["product_detail"].format(slug=slug)
            cache.delete(detail_cache_key)
            messages.success(request, 'Thank you for your valuable feedback!')
            return redirect('product_detail', slug=product.slug)

        related_products = list(
            Product.objects.filter(
                category=product.category,
                is_available=True
            ).exclude(id=product.id).select_related('category').only(
                'id', 'name', 'slug', 'short_description', 'price', 'stock',
                'minimum_order_quantity', 'image', 'secondary_image',
                'is_featured', 'created_at', 'category__id', 'category__name'
            )[:4]
        )
        context = {
            'product': product,
            'related_products': related_products,
        }
        return render(request, 'products/product_detail.html', context)

    # ─── GET: Product detail (cached per slug) ───
    detail_cache_key = CACHE_KEYS["product_detail"].format(slug=slug)
    cached_context = cache.get(detail_cache_key)

    if cached_context is not None:
        return render(request, 'products/product_detail.html', cached_context)

    product = get_object_or_404(
        Product.objects.select_related('category').prefetch_related('gallery', 'reviews'),
        slug=slug,
        is_available=True
    )

    related_products = list(
        Product.objects.filter(
            category=product.category,
            is_available=True
        ).exclude(id=product.id).select_related('category').only(
            'id', 'name', 'slug', 'short_description', 'price', 'stock',
            'minimum_order_quantity', 'image', 'secondary_image',
            'is_featured', 'created_at', 'category__id', 'category__name'
        )[:4]
    )

    context = {
        'product': product,
        'related_products': related_products,
    }

    cache.set(detail_cache_key, context, TTL_MEDIUM)
    return render(request, 'products/product_detail.html', context)


def search(request):
    query = request.GET.get('q', '')
    products_list = Product.objects.filter(is_available=True).select_related('category').only(
        'id', 'name', 'slug', 'short_description', 'price', 'stock',
        'minimum_order_quantity', 'image', 'secondary_image',
        'is_featured', 'created_at', 'category__id', 'category__name'
    )
    
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        )
        
    categories = cache.get(CACHE_KEYS["all_categories"])
    if categories is None:
        categories = list(Category.objects.filter(is_active=True).only('id', 'name', 'slug'))
        cache.set(CACHE_KEYS["all_categories"], categories, TTL_LONG)

    total_products_count = cache.get(CACHE_KEYS["available_count"])
    if total_products_count is None:
        total_products_count = Product.objects.filter(is_available=True).count()
        cache.set(CACHE_KEYS["available_count"], total_products_count, TTL_SHORT)

    # Sorting
    current_sort = request.GET.get('sort', 'recommended')
    if current_sort == 'price_asc':
        products_list = products_list.order_by('price')
    elif current_sort == 'price_desc':
        products_list = products_list.order_by('-price')
    elif current_sort == 'newest':
        products_list = products_list.order_by('-created_at')
    else:  # recommended
        products_list = products_list.order_by('-is_featured', '-created_at')

    # Pagination
    paginator = Paginator(products_list, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'total_products_count': total_products_count,
        'current_sort': current_sort,
        'search_query': query,
        'active_category': None,
    }
    return render(request, 'products/product_list.html', context)
