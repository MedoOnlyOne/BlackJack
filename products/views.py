from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Product,Review
import requests 
import decimal
from decouple import config
# Create your views here.

def index(request):
    return render(request, 'products/index.html',{
        'products': Product.objects.all()
    })


def product(request, productid):
    if request.method=='POST':
        if 'add_review' in request.POST:
            text=request.POST.get('review','')
            rating=request.POST.get('rate',1)
            u = request.user
            rev=Review(text=text,stars=rating, user=u)
            rev.save()
            product=Product.objects.get(id=productid)
            product.reviews.add(rev)
            return HttpResponseRedirect(reverse('productpage',args=[productid]))

        elif 'add_to_cart' in request.POST:
            if request.user.is_authenticated:
                product_name = request.POST['productname']
                product = Product.objects.get(name=product_name)
                request.user.cart.add(product)

                return HttpResponseRedirect(reverse('productpage',args=[productid]))
            else:
                return HttpResponseRedirect(reverse('login'))
        elif 'add_to_wishlist' in request.POST:
            if request.user.is_authenticated:
                product_name = request.POST['productname']
                product = Product.objects.get(name=product_name)
                request.user.wishlist.add(product)

                return HttpResponseRedirect(reverse('productpage',args=[productid]))
            else:
                return HttpResponseRedirect(reverse('login'))
    else:
        try:
            product = Product.objects.get(id=productid)
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
            if request.user.is_authenticated:
                in_wishlist=product in request.user.wishlist.all()
                in_cart=product in request.user.cart.all()
            else:
                in_wishlist=None
                in_cart=None
            return render(request,'products/product.html',{
            'product': product,
            'rating': rating,
            'price' : round(product.price*decimal.Decimal(currency_ratio),2),
            'preferred_currency':preferred_currency,
            'reviews':reviews,
            'in_wishlist':in_wishlist,
            'in_cart': in_cart
            })
        except (Product.DoesNotExist,ValidationError) :
            return render(request,'products/404.html')
        
    
    

