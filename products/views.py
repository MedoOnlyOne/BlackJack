from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Product,Review
import requests 
import decimal
from decouple import config
# Create your views here.

def index(request):
    return render(request, 'products/index.html',{
        'products': Product.objects.all()
    })


def product(request, productname):
    if request.method=='POST':
        text=request.POST.get('review','')
        rating=request.POST.get('rate',1)
        rev=Review(text=text,stars=rating)
        rev.save()
        product=Product.objects.get(name=productname)
        product.reviews.add(rev)
        return HttpResponseRedirect(reverse('products:productpage',args=[productname]))
    else:
        product = Product.objects.get(name=productname)
        if not request.user.is_authenticated:
            currency_ratio=1
            preferred_currency='EGP'
        else:
            preferred_currency=request.user.preferred_currency
            if preferred_currency=='EGP':
                currency_ratio=1
            else:
                #currency_ratio=requests.get('https://free.currconv.com/api/v7/convert',{'apiKey':config('API_KEY'),'q':'EGP'+'_'+preferred_currency,'compact':'ultra'}).json()['EGP'+'_'+preferred_currency]
                currency_ratio=1
        rating = 0
        reviews = product.reviews.all()
        for rev in reviews:
            rating += rev.stars
        if len(reviews) > 0:
            rating /= len(reviews)
        else:
            rating = 0
        return render(request,'products/product copy.html',{
        'product': product,
        'rating': rating,
        'price' : round(product.price*decimal.Decimal(currency_ratio),2),
        'preferred_currency':preferred_currency
        })
    

