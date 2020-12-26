from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Shop, Coupon
from products.models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#from django.db import TypeError

def index(request, shopname):
    try:
    #if shopname in Shop.objects.all():
        if shopname=='addproduct':
            return addproduct(request)
        shop = Shop.objects.get(name=shopname)
        products = shop.products.all()
        return render(request, 'shop/index.html',{
            'shop': shop,
            'products': products
        })
    except Shop.DoesNotExist:
        return render(request,'shop/404.html')

@login_required()
def addproduct(request):
    if request.method=='GET':
        if request.user.shop:
            return render(request,'shop/AddProduct.html',{
                'shop': request.user.shop
            })
        else:
            return render(request,'shop/not_a_seller.html')
    else:
        name = request.POST.get('product','')
        price = request.POST.get('price','')
        remaining = request.POST.get('remaining_in_stock','')
        disc = request.POST.get('discription','')
        img = request.FILES.get('image')
        print(f"### {name}  {price} {remaining} {disc}  {img}   ##############")
        shop = Shop.objects.get(name=request.user.shop)
        p = Product(name=name,image=img,price=price,description=disc,remaininginstock=remaining,featured=False,shop=shop)
        p.save()
        print(f"### {p.name}  {p.price} {p.remaininginstock} {p.description}  #################")
        shop.products.add(p)

        return HttpResponseRedirect(reverse('shopdashboard'))


@login_required
def editproduct(request, productid):
    if request.method == "GET":
        return render(request,'shop/EditProduct.html',{
            'product':Product.objects.get(id=productid)
        })
    else:
        name = request.POST.get('product','')
        price = request.POST.get('price','')
        remaining = request.POST.get('remaining_in_stock','')
        disc = request.POST.get('description','')
        p = Product.objects.get(id=productid)
        p.name = name
        p.price = price
        p.description = disc
        p.remaininginstock = remaining
        p.save()
        return HttpResponseRedirect(reverse('shopdashboard'))

@login_required
def dashboard(request):
    if request.user.shop:
        return render(request,'shop/Dashboard.html',{
            'shop':request.user.shop,
            'products' : request.user.shop.products.all()
        })
    else:
        return render(request,'shop/not_a_seller.html')

@login_required
def addcoupon(request):
    if request.method == "GET":
        active_coupons = []
        coupons = request.user.shop.coupons.all()
        for coupon in coupons:
            if coupon.activated:
                active_coupons.append(coupon)
        return render(request, 'shop/AddCoupon.html',{
            'coupons': active_coupons
        })
    else:
        name = request.POST.get('name','')
        code = request.POST.get('code','')
        discount = request.POST.get('discount','')
        c = Coupon(name=name, code=code, activated=True, discount=discount)
        c.save()
        request.user.shop.coupons.add(c)
        return HttpResponseRedirect(reverse('addcoupon'))

@login_required
def deactivatecoupon(request, couponid):
    c = Coupon.objects.get(code=couponid)
    c.activated = False
    c.save()
    return HttpResponseRedirect(reverse('addcoupon'))