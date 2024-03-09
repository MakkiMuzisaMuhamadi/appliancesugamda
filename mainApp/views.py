from django import forms
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render,  get_object_or_404
from mainApp.forms import ProductForm
from mainApp.models import *
from django.shortcuts import render, redirect
from .forms import BrandForm, CategoryForm, ProductForm
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.sessions.backends.db import SessionStore
from datetime import datetime, timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout

def login(request):
    error_message = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_staff:
                auth_login(request, user)
                return redirect('admin-applianceuganda')
            else:
                return redirect('index')
        else:
            error_message = 'Invalid username or password'
    return render(request, 'login.html', {'error_message': error_message})

def logout_view(request):
    logout(request)
    return redirect('login')

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
def shopDetail(request):
    categories = Category.objects.all()
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_items_count = sum(item.quantity for item in cart_items)
    request.session['cart_items_count'] = cart_items_count

    context = {
        'categories': categories,
         }   
    return render (request, 'shopDetail.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    cart_items_count = sum(item.quantity for item in cart_items)
    request.session['cart_items_count'] = cart_items_count
    categories = Category.objects.all()

    context = {
        'product': product,
        'categories': categories,

    }
    return render(request, 'detail.html', context)
def product_search(request):
    query = request.GET.get('q', '')

    # Filter products based on the search query
    products = Product.objects.filter(
        models.Q(name__icontains=query)
        # models.Q(category__name__icontains=query) | 
        # models.Q(brand__name__icontains=query) 
    )
    categories = Category.objects.all()

    context = {
        'products': products,
        'query': query,
        'categories': categories,
    }

    return render(request, 'search.html', context)

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

def get_cart_count(request):
    session_key = request.session.session_key
    cart_count = CartItem.objects.filter(session_key=session_key).count()
    return JsonResponse({'count': cart_count})

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
    categories = Category.objects.all()
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': categories,
    }
    return render(request, 'cart.html', context)



def checkout(request):
    session_key = request.session.session_key
    cart_items = CartItem.objects.filter(session_key=session_key)
    categories = Category.objects.all()
    # Calculate total price for each item in the cart
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    # Calculate the final total of all products
    total_price = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'categories': categories,
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
        country=request.POST.get('country'),
        total_price=total_price
    )
    order.save() 
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            image=cart_item.product.image,
            price=cart_item.product.price
        )

    cart_items.delete()
    messages.success(request, 'Your Order has been received, We shall contact you soon')
    return redirect('index')

def buy_now(request):
    order2 = BuyNow2.objects.create(
        name = request.POST.get('name'),
        phone_number = request.POST.get('phone_number'),
        product_name = request.POST.get('product_name'),
        product_price = request.POST.get('product_price'),
        product_id = request.POST.get('product_id'),
        product_brand = request.POST.get('product_brand'),
        product_category = request.POST.get('product_category'),
    )
    order2.save()

    messages.success(request, 'Your Order has been received, We shall contact you soon')
    return redirect('index')

def category_products(request, category_id):
    categories = Category.objects.all()
    category2 = get_object_or_404(Category, id=category_id)
    products = Product.objects.filter(category=category2)
    context = {
        'category2': category2,
        'categories': categories,
        'products': products,
        }
    return render(request, 'category_products.html', context)


# admin side views
@login_required
def admin1(request):
    products2 = Product.objects.all()
    categories = Category.objects.all()
    orders = Order.objects.all()
    brands = Brand.objects.all()
    context = {
        'categories': categories,
        'orders': orders,
        'products': products2,
        'brands': brands,
         }   
    return render (request, 'admin1/index.html', context)
@login_required
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
    return render(request, 'admin1/products.html', {'form': form})
@login_required
def get_brands(request):
    category_id = request.GET.get('category_id')
    brands = Brand.objects.filter(category_id=category_id).values('id', 'name')
    return JsonResponse(list(brands), safe=False)
@login_required
def productList(request):
    products = Product.objects.all()
    
    context = {
        'products': products,
         }   
    return render (request, 'admin1/viewproduct.html', context)
@login_required
def categoryList(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
         }   
    return render (request, 'admin1/categoryList.html', context)
@login_required
def brandList(request):
    brands = Brand.objects.all()
    context = {
        'brands': brands,
         }   
    return render (request, 'admin1/brandList.html', context)
@login_required
def delete_product(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        product = Product.objects.get(id=product_id)
        product.delete()
    messages.success(request, 'Product Deleted Successfully')
    return redirect('productList')
@login_required
def delete_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        category.delete()
    messages.success(request, 'Category Deleted Successfully')
    return redirect('categoryList')
@login_required
def delete_brand(request):
    if request.method == 'POST':
        brand_id = request.POST.get('brand_id')
        brand = Brand.objects.get(id=brand_id)
        brand.delete()
    messages.success(request, 'Brand Deleted Successfully')
    return redirect('brandList')
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('categoryList')  
    else:
        form = CategoryForm()
    return render(request, 'admin1/add_category.html', {'form': form})
@login_required
def add_brand(request):
    if request.method == 'POST':
        form = BrandForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('brandList') 
    else:
        form = BrandForm()
    return render(request, 'admin1/add_brand.html', {'form': form})
@login_required
def order_list(request):
    # Get orders ordered by creation date in descending order
    orders = Order.objects.order_by('-created_at')

    # Get the current date
    current_date = datetime.now()

    # Calculate the date one day ago
    one_day_ago = current_date - timedelta(days=1)

    return render(request, 'admin1/orders.html', {'orders': orders, 'one_day_ago': one_day_ago})
def delete_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id)
        order.delete()
    messages.success(request, 'Order Deleted Successfully')
    return redirect('order_list')

def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin1/orderDetails.html', {'order': order})


def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)  # Include request.FILES
        if form.is_valid():
            form.save()
            return redirect('productList')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin1/edit_product.html', {'form': form})