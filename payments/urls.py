from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('pay/<uuid:order_id>/', views.payment_page, name='payment_page'),
    path('upload-screenshot/<uuid:order_id>/', views.upload_payment_screenshot, name='upload_screenshot'),
    path('cod/<uuid:order_id>/', views.cod_order, name='cod_order'),
    path('verify/<uuid:payment_id>/', views.verify_payment, name='verify_payment'),
]
