from django.contrib import admin
from Store.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'ProductID',
        'ProductName',
        'Description',
        'Price',
        'image'
    ]

class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        'CustomerID',
        'CustomerName',
        'CustomerContact',
        'CustomerAddress'
    ]

class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'SessionOrderID', 
        'OrderID',
        'CustomerID_id',
        'ProductID_id', 
        'ProductName',
        'Quantity',
        'TotalPrice'
    ]

# Register all models with the admin interface
admin.site.register(ProductDetails, ProductAdmin)
admin.site.register(CustomerDetails, CustomerAdmin)
admin.site.register(OrderDetails, OrderAdmin)