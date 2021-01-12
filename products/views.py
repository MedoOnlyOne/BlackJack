from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.exceptions import ValidationError
from .models import Product,Review
import requests 
import decimal
import random,os
# Create your views here.
currency_symbols={
    'EGP':'EGP',
    'EUR':'€',
    'USD':'$',
    'GBP':'£'
}

currency_names={
    'EGP':'Egyptian Pound',
    'EUR':'Euro',
    'USD':'US Dollars',
    'GBP':'English Pounds'
}
def get_currency_ratio(request):
    preferred_currency=get_preffered_currency(request)
    if preferred_currency=='EGP':
        return 1
    else:
        return requests.get('https://free.currconv.com/api/v7/convert',{'apiKey':os.environ.get('API_KEY'),'q':'EGP'+'_'+preferred_currency,'compact':'ultra'}).json()['EGP'+'_'+preferred_currency]

def get_preffered_currency(request):
    if not request.user.is_authenticated:
        return 'EGP'
    if request.user.preferred_currency=='':
        return 'EGP'
    return request.user.preferred_currency

    
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
                product_id = request.POST['productid']
                product = Product.objects.get(id=product_id)
                request.user.cart.add(product)

                return HttpResponseRedirect(reverse('productpage',args=[productid]))
            else:
                return HttpResponseRedirect(reverse('login'))
        elif 'add_to_wishlist' in request.POST:
            if request.user.is_authenticated:
                product_id = request.POST['productid']
                product = Product.objects.get(id=product_id)
                request.user.wishlist.add(product)

                return HttpResponseRedirect(reverse('productpage',args=[productid]))
            else:
                return HttpResponseRedirect(reverse('login'))
    else:
        try:
            product = Product.objects.get(id=productid)
            visits = product.visits
            if visits >= 99:
                product.featured = True
            product.visits = visits + 1
            product.save()
            r_products = list(Product.objects.filter(category=product.category))
            r_products.remove(product)
            featured = []
            related = []
            if len(r_products) <= 4:
                related = r_products
            else:
                for p in r_products:
                    if p.featured:
                        featured.append(p)
                if len(featured) == 4:
                    related = featured
                elif len(featured) < 4:
                    while len(featured) < 4:
                        random_product = random.choice(r_products)
                        if random_product not in featured:
                            featured.append(random_product)
                    related = featured
                else:
                    while len(related) < 4:
                        random_product = random.choice(featured)
                        if random_product not in related:
                            related.append(random_product)
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
            is_user_product=False
            if request.user:
                if request.user.is_authenticated and request.user.shop:
                    if product.shop.id==request.user.shop.id:
                        is_user_product=True
            user_has_review=False
            if request.user.is_authenticated:
                if Review.objects.filter(user=request.user,reviews=product):
                    user_has_review=True
            return render(request,'products/product.html',{
            'product': product,
            'rating': rating,
            'currency_ratio': get_currency_ratio(request),
            'preferred_currency':get_preffered_currency(request),
            'currency_symbol':currency_symbols[get_preffered_currency(request)],
            'reviews':reviews,
            'in_wishlist':in_wishlist,
            'in_cart': in_cart,
            'is_user_product':is_user_product,
            'user_has_review':user_has_review,
            'related':related,
            'related_len':len(related),
            'currency_ratio':get_currency_ratio(request),
            'currency_name':currency_names[get_preffered_currency(request)]
            })
        except (Product.DoesNotExist,ValidationError) :
            return render(request,'products/404.html')
        
    
    

