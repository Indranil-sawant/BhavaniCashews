from django.shortcuts import render, get_object_or_404, redirect 
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Category, Product, ProductGallery, ProductReview
from django.contrib.auth.decorators import login_required

def home(request):
    featured_products = Product.objects.filter(
        is_featured=True,
        is_available=True
    ).select_related('category')[:6]

    newest_products = Product.objects.filter(
        is_available=True
    ).select_related('category').order_by('-created_at')[:6]

    categories = Category.objects.filter(is_active=True)
    available_products_count = Product.objects.filter(is_available=True).count()
    featured_products_count = Product.objects.filter(is_featured=True, is_available=True).count()

    context = {
        'featured_products': featured_products,
        'newest_products': newest_products,
        'categories': categories,
        'available_products_count': available_products_count,
        'featured_products_count': featured_products_count,
    }

    return render(request, 'products/home.html', context)


def product_list(request):
    products_list = Product.objects.filter(is_available=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    total_products_count = products_list.count()

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
        'active_category': None,
    }
    return render(request, 'products/product_list.html', context)


def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug, is_active=True)
    products_list = Product.objects.filter(category=category, is_available=True).select_related('category')
    categories = Category.objects.filter(is_active=True)
    total_products_count = Product.objects.filter(is_available=True).count()

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
        'active_category': category,
    }
    return render(request, 'products/product_list.html', context)

@login_required
def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.prefetch_related('gallery', 'reviews'),
        slug=slug,
        is_available=True
    )
    
    if request.method == 'POST':
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
            messages.success(request, 'Thank you for your valuable feedback!')
            return redirect('product_detail', slug=product.slug)
            
    related_products = Product.objects.filter(
        category=product.category,
        is_available=True
    ).exclude(id=product.id).select_related('category')[:4]

    context = {
        'product': product,
        'related_products': related_products,
    }
    return render(request, 'products/product_detail.html', context)


def search(request):
    query = request.GET.get('q', '')
    products_list = Product.objects.filter(is_available=True).select_related('category')
    
    if query:
        products_list = products_list.filter(
            Q(name__icontains=query) |
            Q(sku__icontains=query) |
            Q(short_description__icontains=query) |
            Q(description__icontains=query)
        )
        
    categories = Category.objects.filter(is_active=True)
    total_products_count = Product.objects.filter(is_available=True).count()

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

@login_required
def checkout(request):
    """Renders the secure checkout page."""
    return render(request, 'products/checkout.html')