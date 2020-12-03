from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Shop
from products.models import Product
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#from django.db import TypeError

def index(request, shopname):
    try:
    #if shopname in Shop.objects.all():
        shop = Shop.objects.get(name=shopname)
        products = shop.products.all()
        try:
            usershops=request.user.shops.all()
        except:
            usershops=None
        return render(request, 'shop/index.html',{
            'shop': shop,
            'products': products,
            'usershops':usershops
        })
    except Shop.DoesNotExist:
        return HttpResponse('<h1>Shop does Not Exist!</h1>')

@login_required()
def addproduct(request,shopname):
    if request.method=='GET':
        if Shop.objects.get(name=shopname) in request.user.shops.all():
            return render(request,'shop/AddProduct.html',{
                'shopname': shopname
            })
        else:
            return HttpResponse('<h1>Access Denied<h1>')
    else:
        name = request.POST['productname']
        img = request.FILES['img']
        p = Product(name=name,image=img,price=100,description='aaaa',remaininginstock=1,featured=False)
        p.save()
        shop = Shop.objects.get(name=shopname)
        shop.products.add(p)

        return HttpResponseRedirect(reverse('dashboard',args=[shop.name]))