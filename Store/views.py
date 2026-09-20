from django.shortcuts import render, HttpResponseRedirect
from .models import CustomerDetails, ProductDetails, OrderDetails
import sqlite3

def index_view(request):
    products = ProductDetails.objects.all()
    data = {'Products':products}
    return render(request,'index.html', data)

def add_to_cart_view(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    product_name = request.GET.get('productName')
    product_price = request.GET.get('productPrice')
    product_qty = int(request.GET.get('quantity'))
    cur.execute('SELECT ProductID, image FROM Store_productdetails WHERE ProductName = ?;', (product_name,))
    product_id_image = cur.fetchone()
    print(product_id_image)
    conn.close()
    
    # Check if this product already exists in cart (no CustomerID means it's a cart item)
    existing_cart_item = OrderDetails.objects.filter(
        ProductName=product_name, 
        CustomerID_id__isnull=True
    ).first()
    
    if existing_cart_item:
        # Product already in cart - update quantity and total
        existing_cart_item.Quantity += product_qty
        existing_cart_item.TotalPrice = float(product_price) * existing_cart_item.Quantity
        existing_cart_item.save()
    else:
        # Product not in cart - create new entry
        total = float(product_price) * product_qty
        OrderDetails.objects.create(
            ProductName=product_name, 
            Quantity=product_qty, 
            TotalPrice=total, 
            image=product_id_image[1],
            ProductID_id=product_id_image[0]
        )
    
    return HttpResponseRedirect('/cart/')

def remove_pro(request, id):
    if request.method == "POST":
        # Only delete cart items, not completed orders
        OrderDetails.objects.filter(ProductID_id=id, CustomerID_id__isnull=True).delete()
        return HttpResponseRedirect('/cart/')

def update_pro(request):
    product_name = request.GET.get('productName')
    new_product_qty = int(request.GET.get('quantity'))
    
    # Only update cart items, not completed orders
    cart_item = OrderDetails.objects.filter(ProductName=product_name, CustomerID_id__isnull=True).first()
    if cart_item:
        cart_item.Quantity = new_product_qty
        # Recalculate total based on product price
        product = ProductDetails.objects.get(ProductName=product_name)
        cart_item.TotalPrice = product.Price * new_product_qty
        cart_item.save()
    
    return HttpResponseRedirect('/cart/')

def cart_view(request):
    # Only show cart items, not completed orders
    cart_products = OrderDetails.objects.filter(CustomerID_id__isnull=True)
    
    # Calculate total only for cart items
    total = sum(item.TotalPrice for item in cart_products)
    
    data = {'cart':cart_products, 'total':total}
    return render(request, 'cart.html', data)

def checkout_view(request):
    return render(request, 'checkout.html')

def contact(request):
    return render(request, 'contact.html')

def about(request):
    return render(request, 'about.html')

def order_confirmation_view(request):
    conn = sqlite3.connect('db.sqlite3')
    cur = conn.cursor()
    if request.method == 'POST':
        cus_name = request.POST.get('customerName')
        cus_contact = request.POST.get('customerContact')
        cus_address = request.POST.get('customerAddress')
        
        # Check if customer with this contact number already exists
        existing_customer = CustomerDetails.objects.filter(CustomerContact=cus_contact).first()
        
        if existing_customer:
            customer = existing_customer
        else:
            # Create new customer only if they don't exist
            customer = CustomerDetails.objects.create(
                CustomerName=cus_name, 
                CustomerContact=cus_contact, 
                CustomerAddress=cus_address
            )
    import uuid
    session_order_id = str(uuid.uuid4())[:8]  
    
    # Update only current cart items with the same SessionOrderID and Customer ID
    OrderDetails.objects.filter(CustomerID_id__isnull=True).update(CustomerID_id=customer.CustomerID, SessionOrderID=session_order_id)
    items = OrderDetails.objects.filter(CustomerID_id=customer.CustomerID, SessionOrderID=session_order_id)
    # Calculate total only for current order items
    total = sum(item.TotalPrice for item in items)
    
    remaining_cart_items = OrderDetails.objects.filter(CustomerID_id__isnull=True)
    remaining_cart_items.delete()
    
    conn.close()
    data = {'customer':customer, 'items':items, 'total':total}
    return render(request, 'order-confirmation.html', data)