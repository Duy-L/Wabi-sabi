from django.shortcuts import render, redirect
from products.models import Product

from .models import Cart

#this function calculates all of the products that are currently in the cart 
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = cart_obj.products.active()
    total = 0
    for x in products:
        total += x.price
    print(total)
    cart_obj.total = total
    cart_obj.save()
    return render(request, "carts/home.html", {"cart": cart_obj}) 

#add to cart functionality
def cart_update_add(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj not in cart_obj.products.active():
            cart_obj.products.add(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
        return redirect(request.META['HTTP_REFERER'])
    
# remove from cart functionality
def cart_update_remove(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.active():
            cart_obj.products.remove(product_obj)
        request.session['cart_items'] = cart_obj.products.count()
         
        return redirect(request.META['HTTP_REFERER'])

#clear the cart
def cart_clear (request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print("Show message to user, product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
           cart_obj.clear()
        request.session['cart_items'] = cart_obj.products.count()

        return redirect(request.META['HTTP_REFERER'])