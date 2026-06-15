from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.api.views import (
    CategoryViewSet,
    CashewGradeViewSet,
    ProductViewSet,
    ProductReviewViewSet,
    HomeAPIView
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'grades', CashewGradeViewSet, basename='cashewgrade')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ProductReviewViewSet, basename='productreview')

urlpatterns = [
    path('', include(router.urls)),
    path('home/', HomeAPIView.as_view(), name='home-api'),
]
