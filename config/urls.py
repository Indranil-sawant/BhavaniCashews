"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from config import settings

# ─── Admin Branding ───
admin.site.site_title = getattr(settings, 'ADMIN_SITE_TITLE', 'Bhavani Cashews Admin')
admin.site.site_header = getattr(settings, 'ADMIN_SITE_HEADER', 'Bhavani Cashews')
admin.site.index_title = getattr(settings, 'ADMIN_INDEX_TITLE', 'Command Centre')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('products.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('cart/', include('cart.urls')),
    path('orders/', include('orders.urls')),
    path('payments/', include('payments.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)