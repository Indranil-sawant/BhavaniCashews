import datetime
from django import template
from django.db.models import Sum, Count, Q
from django.db.models.functions import TruncMonth
from django.utils import timezone
from django.contrib.auth import get_user_model
from orders.models import Order, OrderStatus, PaymentStatus
from products.models import Product, CashewGrade, Category

User = get_user_model()
register = template.Library()

@register.simple_tag
def get_dashboard_data():
    today = timezone.now()
    
    # KPIs
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(
        status__in=[OrderStatus.PLACED, OrderStatus.CONFIRMED, OrderStatus.SHIPPED]
    ).count()
    completed_orders = Order.objects.filter(status=OrderStatus.DELIVERED).count()
    
    # Revenue (Paid orders)
    total_revenue = Order.objects.filter(payment_status=PaymentStatus.PAID).aggregate(Sum('total'))['total__sum'] or 0
    
    # Customer Count
    customers = User.objects.filter(is_staff=False).count()
    
    # Stock Alert systems
    low_stock_products_count = Product.objects.filter(stock__lt=10, stock__gt=0).count()
    out_of_stock_products_count = Product.objects.filter(stock=0).count()
    
    # Recent lists
    recent_orders = Order.objects.select_related('shipping_address', 'user').order_by('-created_at')[:5]
    recent_products = Product.objects.select_related('category', 'grade').order_by('-created_at')[:5]
    
    # Inventory lists
    low_stock_products = Product.objects.filter(stock__lt=10).select_related('category', 'grade')[:5]
    out_of_stock_products = Product.objects.filter(stock=0).select_related('category', 'grade')[:5]
    featured_products = Product.objects.filter(is_featured=True).select_related('category', 'grade')[:5]
    available_products = Product.objects.filter(is_available=True).select_related('category', 'grade')[:5]
    
    # Grades with stock levels
    grade_stock = CashewGrade.objects.annotate(
        total_stock=Sum('products__stock')
    ).filter(is_active=True).order_by('-total_stock')
    
    # Quality score (Fake or reviews average)
    quality_rating = "4.9"
    
    # ─── Chart 1 & 2: Last 12 Months Revenue & Orders ───
    # Calculate starting point (12 months ago)
    first_day_current_month = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start_date = first_day_current_month - datetime.timedelta(days=365)
    
    monthly_stats = Order.objects.filter(
        created_at__gte=start_date
    ).annotate(
        month=TruncMonth('created_at')
    ).values('month').annotate(
        revenue=Sum('total', filter=Q(payment_status=PaymentStatus.PAID)),
        order_count=Count('id')
    ).order_by('month')
    
    # Generate continuous list of past 12 months to avoid empty month gaps
    months_labels = []
    revenue_data = []
    orders_data = []
    
    # Generate list of month datetimes
    for i in range(11, -1, -1):
        # Subtract months
        m_date = first_day_current_month - datetime.timedelta(days=i*30) # approximate
        # Correct to the actual start of that month to align with TruncMonth
        m_date = m_date.replace(day=1)
        months_labels.append(m_date.strftime('%b %Y'))
        
        # Search in monthly_stats
        found_revenue = 0
        found_orders = 0
        for stat in monthly_stats:
            if stat['month'] and stat['month'].year == m_date.year and stat['month'].month == m_date.month:
                found_revenue = float(stat['revenue'] or 0)
                found_orders = int(stat['order_count'] or 0)
                break
        revenue_data.append(found_revenue)
        orders_data.append(found_orders)
        
    # ─── Chart 3: Product Distribution by Category ───
    category_stats = Category.objects.annotate(
        product_count=Count('products')
    ).values('name', 'product_count')
    category_labels = [c['name'] for c in category_stats]
    category_values = [c['product_count'] for c in category_stats]
    
    # ─── Chart 4: Product Distribution by Grade ───
    grade_stats = CashewGrade.objects.annotate(
        product_count=Count('products')
    ).values('name', 'product_count')
    grade_labels = [g['name'] for g in grade_stats]
    grade_values = [g['product_count'] for g in grade_stats]
    
    return {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_revenue': total_revenue,
        'customers': customers,
        'low_stock_products_count': low_stock_products_count,
        'out_of_stock_products_count': out_of_stock_products_count,
        'recent_orders': recent_orders,
        'recent_products': recent_products,
        'low_stock_products': low_stock_products,
        'out_of_stock_products': out_of_stock_products,
        'featured_products': featured_products,
        'available_products': available_products,
        'grade_stock': grade_stock,
        'quality_rating': quality_rating,
        
        # Chart JSON data list helpers
        'months_labels': months_labels,
        'revenue_data': revenue_data,
        'orders_data': orders_data,
        'category_labels': category_labels,
        'category_values': category_values,
        'grade_labels': grade_labels,
        'grade_values': grade_values,
    }
