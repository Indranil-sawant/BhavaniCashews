from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile_view, name='profile'),
    path('addresses/create/', views.address_create, name='address_create'),
    path('addresses/edit/<int:pk>/', views.address_edit, name='address_edit'),
    path('addresses/delete/<int:pk>/', views.address_delete, name='address_delete'),
    path('addresses/default/<int:pk>/', views.address_set_default, name='address_set_default'),
]