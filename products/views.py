from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product
from django.db.models import Q 
import requests 
import decimal
from decouple import config
# Create your views here.
def index(request):
    return render(request, 'products/index.html',{
        'products': Product.objects.all()
    })


def product(request, productname):
    product = Product.objects.get(name=productname)
    if not request.user.is_authenticated:
        currency_ratio=1
    else:
        preferred_currency=request.user.preferred_currency
        if preferred_currency=='EGP':
            currency_ratio=1
        else:
            currency_ratio=requests.get('https://free.currconv.com/api/v7/convert',{'apiKey':config('API_KEY'),'q':'EGP'+'_'+preferred_currency,'compact':'ultra'}).json()['EGP'+'_'+preferred_currency]
        
    return render(request,'products/product.html',{
    'product': product,
    'price' : round(product.price*decimal.Decimal(currency_ratio),2),
    'user' : request.user
    })
    # return HttpResponseRedirect(reverse('product',args=[p]))


def search(request):
    query = request.Get['q']
    print(f"###########     {query}   ###############")
    results = Product.objects.filter(Q(name__icontains=query))
    print(f'###############     {results}   ##############')
    return render(request, 'products/searchResult.html',{
        'products': results
    })