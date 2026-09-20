"""
URL configuration for ThreadsAndCo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
    
"""
from django.contrib import admin
from django.urls import path
from Store import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'Store'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name='index'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order-confirmation/', views.order_confirmation_view, name='order-confirmation'),
    path('cart/', views.cart_view, name='cart'),
    path('add-to-cart/', views.add_to_cart_view, name='add_to_cart_view'),
    path('remove_pro/<int:id>/', views.remove_pro, name='remove_pro'),
    path('update_pro/', views.update_pro, name='update_pro'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)