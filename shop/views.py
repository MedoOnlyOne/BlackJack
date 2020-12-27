from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Shop, Coupon
from products.models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import string 
import random 
#from django.db import TypeError

def index(request, shopname):
    try:
    #if shopname in Shop.objects.all():
        if shopname=='addproduct':
            return addproduct(request)
        elif shopname=='activecoupons':
            return activecoupons(request)
        # if request.user.shop and request.user.shop.name == shopname:
        #     return HttpResponseRedirect(reverse('shopdashboard'))
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
        if Coupon.objects.filter(name=name):
             return render(request, 'shop/AddCoupon.html',{
             'message':'Name Already in use'
        })
        letters = string.ascii_letters
        code = ''.join(random.choice(letters) for i in range(5))
        while Coupon.objects.filter(code=code):
            code = ''.join(random.choice(letters) for i in range(5))
        try:
            discount = int(request.POST['discount'])
            if discount>=100:
                  return render(request, 'shop/AddCoupon.html',{
                    'message':'Enter a valid discount percentage'
                  })
            c = Coupon(name=name, code=code, activated=True, discount=discount)
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
    c.activated = False
    c.save()
    return HttpResponseRedirect(reverse('activecoupons'))

@login_required
def activecoupons(request):
    if not request.user.shop:
        return render(request,'shop/not_a_seller.html')
    coupons=request.user.shop.coupons.all()
    if coupons:
        return render(request,'shop/coupons.html',{
            'coupons':coupons
        })
