from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Shop, Coupon
from products.models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import string 
import random 
from decouple import config
import requests


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
    if not request.user.is_authenticated:
        return 1
    preferred_currency=request.user.preferred_currency
    if preferred_currency=='EGP':
        return 1
    else:
        return requests.get('https://free.currconv.com/api/v7/convert',{'apiKey':config('API_KEY'),'q':'EGP'+'_'+preferred_currency,'compact':'ultra'}).json()['EGP'+'_'+preferred_currency]

def get_preffered_currency(request):
    if not request.user.is_authenticated:
        return 'EGP'
    return request.user.preferred_currency


def index(request, shopname):
    try:
    #if shopname in Shop.objects.all():
        if shopname=='addproduct':
            return addproduct(request)
        elif shopname=='activecoupons':
            return activecoupons(request)
        elif shopname=='orders':
            return orders(request)
        shop = Shop.objects.get(name=shopname)
        products = shop.products.all() 
        currency_ratio=get_currency_ratio(request)
        return render(request, 'shop/index.html',{
            'shop': shop,
            'products': products,
            'currency_ratio':currency_ratio,
            'currency_symbol':currency_symbols[get_preffered_currency(request)]
        })
    except Shop.DoesNotExist:
        return render(request,'shop/404.html')

@login_required()
def addproduct(request):
    if request.method=='GET':
        if request.user.shop:
            return render(request,'shop/AddProduct.html',{
                'shop': request.user.shop,
                'currency_name': currency_names[get_preffered_currency(request)]
            })
        else:
            return render(request,'shop/not_a_seller.html')
    else:
        name = request.POST.get('product','')
        cat = request.POST.get('cat','')
        price = request.POST.get('price','')
        price = float(price) / get_currency_ratio(request)
        remaining = request.POST.get('remaining_in_stock','')
        disc = request.POST.get('discription','')
        img = request.FILES.get('image')
        shop = Shop.objects.get(name=request.user.shop)
        p = Product(name=name,image=img,price=price,description=disc,remaininginstock=remaining,category=cat,featured=False,shop=shop)
        p.save()
        shop.products.add(p)
        return HttpResponseRedirect(reverse('shopdashboard'))


@login_required
def editproduct(request, productid):
    if request.method == "GET":
        return render(request,'shop/EditProduct.html',{
            'product':Product.objects.get(id=productid),
            'currency_ratio':get_currency_ratio(request),
            'currency_name':currency_names[get_preffered_currency(request)]
        })
    else:
        name = request.POST.get('product','')
        cat = request.POST.get('cat','')
        price = request.POST.get('price','')
        price = float(price) / get_currency_ratio(request)
        remaining = request.POST.get('remaining_in_stock','')
        disc = request.POST.get('description','')
        p = Product.objects.get(id=productid)
        p.name = name
        p.category = cat
        p.price = price
        p.description = disc
        p.remaininginstock = remaining
        p.save()
        return HttpResponseRedirect(reverse('shopdashboard'))

@login_required
def dashboard(request):
    preferred_currency=get_preffered_currency(request)
    currency_ratio=get_currency_ratio(request)
    if request.user.shop:
        return render(request,'shop/Dashboard.html',{
            'shop':request.user.shop,
            'products' : request.user.shop.products.all(),
            'currency_ratio':currency_ratio,
            'currency_symbol':currency_symbols[preferred_currency]
        })
    else:
        return render(request,'shop/not_a_seller.html')

@login_required
def addcoupon(request):
    if request.method == "GET":
        if not request.user.shop:
            return render(request,'shop/not_a_seller.html')
        coupons = request.user.shop.coupons.all()
        return render(request, 'shop/AddCoupon.html',{
            'coupons': coupons
        })
    else:
        name = request.POST['name']
        if name.isspace() or name=='':
             return render(request, 'shop/AddCoupon.html',{
             'message':'Enter a name'
        })
        coupons=Coupon.objects.filter(name=name)
        if Coupon.objects.filter(name=name):
            for coupon in coupons:
                if coupon.shop.id == request.user.shop.id :
                    return render(request, 'shop/AddCoupon.html',{
                'message':'Name Already in use'
                })
        letters = string.ascii_letters
        code = ''.join(random.choice(letters) for i in range(5))
        while Coupon.objects.filter(code=code):
            code = ''.join(random.choice(letters) for i in range(5))
        try:
            discount = int(request.POST['discount'])
            if discount>=100 and discount<0:
                  return render(request, 'shop/AddCoupon.html',{
                    'message':'Enter a valid discount percentage'
                  })
            c = Coupon(name=name, code=code, activated=True, discount=discount,shop=request.user.shop)
            c.save()
            request.user.shop.coupons.add(c)
            return render(request,'shop/AddCoupon.html',{
                'message':'Entered succesfully',
                'success':True
            })
        except ValueError:
            return render(request, 'shop/AddCoupon.html',{
            'message':'Enter a valid discount percentage'
        })
@login_required
def deactivatecoupon(request, couponid):
    c = Coupon.objects.get(code=couponid)
    c.delete()
    return HttpResponseRedirect(reverse('activecoupons'))

@login_required
def activecoupons(request):
    if not request.user.shop:
        return render(request,'shop/not_a_seller.html')
    coupons=request.user.shop.coupons.all()
    return render(request,'shop/coupons.html',{
            'coupons':coupons
        })
@login_required
def orders(request):
    if not request.user.shop:
        return render(request,'shop/not_a_seller.html')
    return render(request,'shop/orders.html',{'orders':request.user.shop.orders.all(),'shop':request.user.shop})

@login_required
def removefromshop(request,productid):
    product=Product.objects.get(id=productid)
    product.delete()
    return HttpResponseRedirect(reverse('shopdashboard'))