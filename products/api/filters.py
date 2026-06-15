from django_filters import rest_framework as filters
from products.models import Product

class ProductFilter(filters.FilterSet):
    """
    Custom FilterSet for Product querysets.
    Allows filtering by category/grade slugs, price ranges, availability, features, and export quality.
    """
    category = filters.CharFilter(field_name='category__slug', lookup_expr='exact', help_text="Filter by Category slug")
    grade = filters.CharFilter(field_name='grade__slug', lookup_expr='exact', help_text="Filter by Cashew Grade slug")
    price_min = filters.NumberFilter(field_name='price', lookup_expr='gte', help_text="Minimum price filter")
    price_max = filters.NumberFilter(field_name='price', lookup_expr='lte', help_text="Maximum price filter")
    is_featured = filters.BooleanFilter(field_name='is_featured', help_text="Filter by featured status")
    is_available = filters.BooleanFilter(field_name='is_available', help_text="Filter by availability")
    is_export_quality = filters.BooleanFilter(field_name='is_export_quality', help_text="Filter by export quality status")

    class Meta:
        model = Product
        fields = ['category', 'grade', 'price_min', 'price_max', 'is_featured', 'is_available', 'is_export_quality']
