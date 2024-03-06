from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,  get_object_or_404
from mainApp.forms import ProductForm
from mainApp.models import *
from django.shortcuts import render, redirect
from .forms import ProductForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
# Create your views here.
def index(request):
    slide = Slides.objects.all()
    categories = Category.objects.all()
    brands = Brand.objects.all()
    products = Product.objects.all()
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_items_count = sum(item.quantity for item in cart_items)
    request.session['cart_items_count'] = cart_items_count

    context = {
        "slide": slide,
        'categories': categories,
        'brands': brands,
        'products': products,
         }   
    return render (request, 'index.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_items_count = sum(item.quantity for item in cart_items)
    request.session['cart_items_count'] = cart_items_count

    context = {
        'product': product
    }
    return render(request, 'detail.html', context)

#  cart views
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = request.session.session_key
    cart, created = CartItem.objects.get_or_create(session_key=session_key, product=product)

    if not created:
        cart.quantity += 1
        cart.save()

    # Return a JSON response with the message and status
    response_data = {'message': 'Product added to the cart successfully', 'status': 'success'}
    return JsonResponse(response_data)
def cart_detail(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_items_count = sum(item.quantity for item in cart_items)
    # Calculate total price for each item in the cart
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    # Calculate the final total of all products
    total_price = sum(item.total_price for item in cart_items)
    request.session['cart_items_count'] = cart_items_count
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'cart.html', context)



def checkout(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)

    # Calculate total price for each item in the cart
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    # Calculate the final total of all products
    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }

    return render(request, 'checkout.html', context)

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        CartItem.objects.filter(id=item_id).delete()
    return redirect('cart_detail')

def place_order(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    for item in cart_items:
        item.total_price = item.product.price * item.quantity
    total_price = sum(item.total_price for item in cart_items)

    # Create the order
    order = Order.objects.create(
        first_name=request.POST.get('first_name'),
        last_name=request.POST.get('last_name'),
        email=request.POST.get('email'),
        phone=request.POST.get('phone'),
        address=request.POST.get('address'),
        city=request.POST.get('city'),
        country=request.POST.get('country')
    )
    order.save() 
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
        )

    cart_items.delete()
    messages.success(request, 'Your Order has been received, We shall contact you soon')
    return redirect('index')





# admin side views

def adminview(request):
    categories = Category.objects.all()
    
    context = {
        'categories': categories,
         }   
    return render (request, 'admin2/index.html', context)


def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = ProductForm()
    return render(request, 'admin2/products.html', {'form': form})
def get_brands(request):
    category_id = request.GET.get('category_id')
    brands = Brand.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(brands), safe=False)