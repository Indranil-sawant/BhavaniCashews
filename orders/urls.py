from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('success/<uuid:order_id>/', views.order_success, name='order_success'),
    path('detail/<uuid:order_id>/', views.order_detail, name='order_detail'),
    path('list/', views.order_list, name='order_list'),
    path('b2b-inquiry/', views.b2b_inquiry, name='b2b_inquiry'),
]
