from django.db import models
from django.utils.html import mark_safe

def user_directory_path(instance, filename):
    return 'user_(0)/{1}'.format(instance, filename)

class CustomerDetails(models.Model):
    CustomerID = models.AutoField(primary_key=True) 
    CustomerName = models.CharField(max_length=100, null=False)
    CustomerContact = models.CharField(max_length=20, null=False)
    CustomerAddress = models.CharField(max_length=100, null=False)
    def __str__(self):
        return self.CustomerName

class ProductDetails(models.Model):
    ProductID = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=100, null=False)
    Description = models.TextField(null=True, blank=True, help_text="Product description")
    Price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image = models.ImageField(upload_to = user_directory_path, default = 'Product.jpg')
    def __str__(self):
        return self.ProductName
    def product_image(self):
        return mark_safe('<img src="%s" width="250" height="330" />' % (self.image.url))

class OrderDetails(models.Model):
    OrderID = models.AutoField(primary_key=True)
    SessionOrderID = models.CharField(max_length=20, null=True, blank=True)  
    CustomerID = models.ForeignKey(CustomerDetails, on_delete=models.CASCADE, null=True)
    ProductID = models.ForeignKey(ProductDetails, on_delete=models.CASCADE)
    ProductName = models.CharField(max_length=100, null=False)
    Quantity = models.IntegerField(null=False)
    TotalPrice = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    image = models.ImageField(upload_to = user_directory_path, default = 'Product.jpg')

    def __str__(self):
        return f"Order {self.OrderID} - {self.ProductName}"
    def product_image(self):
        return mark_safe('<img src="%s" width="40" height="40" />' % (self.image.url))