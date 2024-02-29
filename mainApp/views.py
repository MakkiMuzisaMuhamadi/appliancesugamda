from django.shortcuts import render
from mainApp.models import *

# Create your views here.
def index(request):
    slide = Slides.objects.all()
    categories = Category.objects.all()
    context = {
        "slide": slide,
        'categories': categories
         }   
    return render (request, 'index.html', context)