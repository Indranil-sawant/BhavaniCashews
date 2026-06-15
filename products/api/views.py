from django.db.models import Avg, Count
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter

from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow administrators (staff) to write reviews.
    Unauthenticated or standard customers can only read reviews.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

from products.models import Category, CashewGrade, Product, ProductReview
from products.api.serializers import (
    CategorySerializer,
    CashewGradeSerializer,
    ProductReviewSerializer,
    ProductListSerializer,
    ProductDetailSerializer,
    HomeAPISerializer
)
from products.api.filters import ProductFilter
from products.api.pagination import StandardResultsSetPagination


@extend_schema_view(
    list=extend_schema(summary="List all categories", description="Retrieve a list of all active cashew product categories."),
    retrieve=extend_schema(summary="Retrieve a category", description="Retrieve details of a specific product category by its ID.")
)
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Category. Offers Read-Only operations.
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer


@extend_schema_view(
    list=extend_schema(summary="List all cashew grades", description="Retrieve a list of all active cashew grades (e.g. W180, W320)."),
    retrieve=extend_schema(summary="Retrieve a cashew grade", description="Retrieve details of a specific cashew grade by its ID.")
)
class CashewGradeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for CashewGrade. Offers Read-Only operations.
    """
    queryset = CashewGrade.objects.filter(is_active=True)
    serializer_class = CashewGradeSerializer


@extend_schema_view(
    list=extend_schema(
        summary="List all products",
        description="Retrieve a paginated, filterable, and searchable list of all products."
    ),
    retrieve=extend_schema(
        summary="Retrieve a product detail",
        description="Retrieve full details of a specific product including category details, grade details, gallery images, and customer reviews."
    )
)
class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Product. Offers Read-Only operations.
    Supports search, ordering, django-filter, and optimized queries.
    """
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    
    search_fields = ['name', 'description', 'short_description', 'category__name']
    ordering_fields = ['price', 'created_at', 'name']
    ordering = ['-is_featured', '-created_at']  # Default ordering

    def get_queryset(self):
        # Base optimized queryset with select_related for foreign keys
        # Annotate average rating and review count directly at DB level to prevent N+1 queries
        queryset = Product.objects.filter(is_available=True).select_related(
            'category', 
            'grade'
        ).annotate(
            annotated_average_rating=Avg('reviews__rating'),
            annotated_review_count=Count('reviews', distinct=True)
        )

        if self.action == 'retrieve':
            # For detail page, prefetch nested gallery and reviews relationship
            queryset = queryset.prefetch_related('gallery', 'reviews')
            
        return queryset

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer

    @extend_schema(summary="Retrieve featured products", description="Get a list of all featured and available cashew products.")
    @action(detail=False, methods=['get'], url_path='featured')
    def featured(self, request):
        queryset = self.get_queryset().filter(is_featured=True)[:10]
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Retrieve new arrivals", description="Get a list of the 10 most recently added products.")
    @action(detail=False, methods=['get'], url_path='new-arrivals')
    def new_arrivals(self, request):
        queryset = self.get_queryset().order_by('-created_at')[:10]
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Retrieve export quality products", description="Get a list of products flagged as export quality.")
    @action(detail=False, methods=['get'], url_path='export-quality')
    def export_quality(self, request):
        queryset = self.get_queryset().filter(is_export_quality=True)
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Retrieve best selling products", description="Get a list of best selling products. Currently orders products by average rating.")
    @action(detail=False, methods=['get'], url_path='best-selling')
    def best_selling(self, request):
        # Ordering by average rating as a proxy for best-selling (or can be customized later)
        queryset = self.get_queryset().order_by('-annotated_average_rating')[:10]
        serializer = ProductListSerializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema_view(
    list=extend_schema(summary="List all reviews", description="Get a list of all product reviews."),
    create=extend_schema(summary="Create a review", description="Add a new review for a product. Requires authentication."),
    retrieve=extend_schema(summary="Retrieve a review", description="Get details of a single review."),
    update=extend_schema(summary="Update a review", description="Modify an existing review. Requires authentication."),
    partial_update=extend_schema(summary="Partially update a review", description="Update specific fields of a review. Requires authentication."),
    destroy=extend_schema(summary="Delete a review", description="Remove a review. Requires authentication.")
)
class ProductReviewViewSet(viewsets.ModelViewSet):
    """
    ViewSet for ProductReview. Allows full CRUD.
    Only admin users can create, update, or delete. Unauthenticated or non-staff users can read.
    """
    queryset = ProductReview.objects.all().select_related('product')
    serializer_class = ProductReviewSerializer
    permission_classes = [IsAdminOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set user name to username if logged in and name is blank
        if not serializer.validated_data.get('name') and self.request.user.is_authenticated:
            serializer.save(name=self.request.user.get_full_name() or self.request.user.username)
        else:
            serializer.save()


class HomeAPIView(APIView):
    """
    Home endpoint. Returns dashboard content containing:
    - categories
    - featured products
    - latest products (new arrivals)
    - export quality products
    """
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Retrieve Home Page Data",
        description="Fetch categories, featured products, latest arrivals, and export quality cashews for the homepage layout.",
        responses={200: HomeAPISerializer}
    )
    def get(self, request, *args, **kwargs):
        # Prefetch optimizations
        categories = Category.objects.filter(is_active=True)[:12]
        
        # Product list queries (pre-optimized with database annotations)
        base_products = Product.objects.filter(is_available=True).select_related(
            'category', 
            'grade'
        ).annotate(
            annotated_average_rating=Avg('reviews__rating')
        )
        
        featured_products = base_products.filter(is_featured=True)[:6]
        latest_products = base_products.order_by('-created_at')[:6]
        export_quality_products = base_products.filter(is_export_quality=True)[:6]

        data = {
            'featured_products': featured_products,
            'categories': categories,
            'latest_products': latest_products,
            'export_quality_products': export_quality_products
        }
        
        serializer = HomeAPISerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)
