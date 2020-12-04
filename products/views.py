from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product

# Create your views here.
def index(request):
    return render(request, 'products/index.html',{
        'products': Product.objects.all()
    })


def product(request, productname):
    p = Product.objects.get(name=productname)
    return render(request,'products/product.html',{
        'product': p
    })
    # return HttpResponseRedirect(reverse('product',args=[p]))