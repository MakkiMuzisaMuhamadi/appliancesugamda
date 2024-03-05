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
    
    context = {
        "slide": slide,
        'categories': categories,
        'brands': brands,
        'products': products,
         }   
    return render (request, 'index.html', context)

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    session_key = request.session.session_key

    # Get or create the cart for the current session
    cart, created = CartItem.objects.get_or_create(session_key=session_key, product=product)

    # Check if product already exists in cart
    if not created:
        cart.quantity += 1
        cart.save()
    messages.success(request, "Product Added to Cart Successfully." )
    return redirect('/')
def cart_detail(request):
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
    return render(request, 'cart.html', context)

def delete_item(request):
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        CartItem.objects.filter(id=item_id).delete()
    return redirect('cart_detail')






def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'detail.html', context)

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
