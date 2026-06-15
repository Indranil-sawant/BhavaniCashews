from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from products.models import Category, CashewGrade, Product, ProductGallery, ProductReview


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']


class CashewGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashewGrade
        fields = ['id', 'name', 'slug', 'description', 'image', 'is_active']


class ProductGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductGallery
        fields = ['id', 'image']


class ProductReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReview
        fields = ['id', 'product', 'name', 'rating', 'review', 'created_at']
        read_only_fields = ['id', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    grade_name = serializers.CharField(source='grade.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'price', 'discount_price', 'image', 
            'stock', 'category_name', 'grade_name', 'average_rating', 
            'is_featured', 'discount_percentage'
        ]

    @extend_schema_field(serializers.FloatField())
    def get_average_rating(self, obj):
        # Optimize by checking if it has been pre-annotated in views
        if hasattr(obj, 'annotated_average_rating') and obj.annotated_average_rating is not None:
            return round(obj.annotated_average_rating, 2)
        
        # Fallback in case queryset was not annotated
        reviews = obj.reviews.all()
        if not reviews:
            return 0.0
        total = sum(review.rating for review in reviews)
        return round(total / len(reviews), 2)

    @extend_schema_field(serializers.FloatField())
    def get_discount_percentage(self, obj):
        if obj.discount_price and obj.price > 0:
            savings = obj.price - obj.discount_price
            percentage = (savings / obj.price) * 100
            return round(percentage, 2)
        return 0.0


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    grade = CashewGradeSerializer(read_only=True)
    gallery = ProductGallerySerializer(many=True, read_only=True)
    reviews = ProductReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'grade', 'gallery', 'reviews', 'name', 'slug',
            'short_description', 'description', 'price', 'discount_price',
            'stock', 'minimum_order_quantity', 'image', 'secondary_image',
            'sku', 'weight', 'packaging_size', 'origin', 'is_export_quality',
            'is_featured', 'is_available', 'created_at', 'updated_at',
            'average_rating', 'review_count', 'discount_percentage'
        ]

    @extend_schema_field(serializers.FloatField())
    def get_average_rating(self, obj):
        if hasattr(obj, 'annotated_average_rating') and obj.annotated_average_rating is not None:
            return round(obj.annotated_average_rating, 2)
        
        reviews = obj.reviews.all()
        if not reviews:
            return 0.0
        total = sum(review.rating for review in reviews)
        return round(total / len(reviews), 2)

    @extend_schema_field(serializers.IntegerField())
    def get_review_count(self, obj):
        if hasattr(obj, 'annotated_review_count'):
            return obj.annotated_review_count
        return obj.reviews.count()

    @extend_schema_field(serializers.FloatField())
    def get_discount_percentage(self, obj):
        if obj.discount_price and obj.price > 0:
            savings = obj.price - obj.discount_price
            percentage = (savings / obj.price) * 100
            return round(percentage, 2)
        return 0.0


class HomeAPISerializer(serializers.Serializer):
    featured_products = ProductListSerializer(many=True)
    categories = CategorySerializer(many=True)
    latest_products = ProductListSerializer(many=True)
    export_quality_products = ProductListSerializer(many=True)
