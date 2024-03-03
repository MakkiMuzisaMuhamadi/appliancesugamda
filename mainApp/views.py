from django.shortcuts import render,  get_object_or_404
from mainApp.models import *

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

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    context = {
        'product': product
    }
    return render(request, 'detail.html', context)