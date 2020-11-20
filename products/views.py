from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product

# Create your views here.
def index(request):
    product = Product.objects.get(name='Test')
    return render(request, 'products/index.html',{
        'product': product
    })