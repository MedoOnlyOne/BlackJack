from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #@login_required(login_url='login/')
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .models import User, Product,Order,InCart
from shop.models import Shop,Coupon
from passlib.hash import django_pbkdf2_sha256
import uuid
from django.conf import settings 
from django.core.mail import send_mail 
import requests,os
from users.models import UserLogin
import datetime,string,random,pytz


currency_symbols={
    'EGP':'EGP',
    'EUR':'€',
    'USD':'$',
    'GBP':'£'
}

def get_currency_ratio(request):
    if not request.user.is_authenticated:
        return 1
    preferred_currency=request.user.preferred_currency
    if preferred_currency=='EGP':
        return 1
    else:
        return requests.get('https://free.currconv.com/api/v7/convert',{'apiKey':os.environ.get('API_KEY'),'q':'EGP'+'_'+preferred_currency,'compact':'ultra'}).json()['EGP'+'_'+preferred_currency]

def get_preffered_currency(request):
    if not request.user.is_authenticated:
        return 'EGP'
    return request.user.preferred_currency

# Create your views here.
@login_required
def cart(request):
    if request.is_ajax():
        coupon_code = request.GET['coupon_code']
        user_coupon = Coupon.objects.filter(code=coupon_code)
        if user_coupon and user_coupon[0].coupon_type=='user':
            if user_coupon[0].activated:
                return JsonResponse({
                    'success': True,
                    'discount': user_coupon[0].discount,
                    'type': 'user'
                })
            return JsonResponse({
                'success':False
            })
        elif user_coupon and user_coupon[0].coupon_type=='event':
            if user_coupon[0].activated:
                return JsonResponse({
                    'success': True,
                    'discount': user_coupon[0].discount,
                    'type': 'event'
                })
            return JsonResponse({
                'success':False
            })    
        else:
            products=request.user.cart.all()
            for product in products:
                for coupon in product.shop.coupons.all():
                    if coupon_code==coupon.code and coupon.activated:
                        return JsonResponse({
                            'success':True,
                            'discount':coupon.discount,
                            'shopname':coupon.shop.name,
                            'type':'shop'
                        })
            return JsonResponse({
                                'success':False
                            })
    elif request.method=='GET':
        preferred_currency=get_preffered_currency(request)
        currency_ratio=get_currency_ratio(request)
        products=request.user.cart.all()
        return render(request,"users/cart.html",
        {
            'currency_ratio':currency_ratio,
            'currency_symbol':currency_symbols[preferred_currency],
            'products':products,
        })
@login_required
def wishlist(request):
    preferred_currency=get_preffered_currency(request)
    currency_ratio=get_currency_ratio(request)
    products=request.user.wishlist.all()
    return render(request,"users/wishlist.html",
    {
        'currency_ratio':currency_ratio,
        'currency_symbol':currency_symbols[preferred_currency],
        'products':products,
        'user':request.user 
    })
@login_required()
def index(request):
    if request.method == "POST":
        first = request.POST.get("first","")
        last = request.POST.get("last", "")
        code = request.POST.get("code", "")
        num = request.POST.get("num", "")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        currency = request.POST.get("currency", "")
        

        user = User.objects.filter(username=request.user.username)
        user.update(first_name=first, last_name=last, phone_number=num, phone_number_code=code, email=email,address=address, preferred_currency=currency)

        return HttpResponseRedirect(reverse("userdashboard"))

    else:
        # Get user's wishList, cart and parchases
        wishlist = request.user.wishlist.all()
        cart = request.user.cart.all()
        shop = request.user.shop
        first_name = request.user.first_name
        last_name = request.user.last_name
        num = request.user.phone_number
        code = request.user.phone_number_code
        email = request.user.email
        currency = request.user.preferred_currency
        address = request.user.address
        is_seller = request.user.is_seller



        return render(request, 'users/Dashboard.html', {
            'wishlist': wishlist,
            'cart': cart,
            'shop':shop,
            'first': first_name,
            'last': last_name,
            'is_seller':is_seller,
            'num': num,
            'code': code,
            'email': email,
            'currency':currency,
            'currency_list': ["EGP","EUR","USD","GBP"],
            'address': address,
        })

def loginview(request):
    if request.method == "POST":
    
        # Try to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            userlogins = UserLogin.objects.filter(user=user)
            timestamps = [login.timestamp for login in userlogins]
            month = 60*60*24*30
            week = 60*60*24*7
            now = datetime.datetime.now(pytz.timezone('Africa/Cairo'))
            timestamps_this_month = [timestamp for timestamp in timestamps if (now-timestamp).total_seconds()<month]    
            days_active_in_this_month = set()
            for timestamp in timestamps_this_month:
                days_active_in_this_month.add(timestamp.day)
            if len(days_active_in_this_month)>=7:
                user_coupon = Coupon.objects.filter(coupon_type='user',name=user.username)
                if not user_coupon and (now-user.date_joined).total_seconds()>month:
                    letters = string.ascii_letters
                    code = ''.join(random.choice(letters) for i in range(5))
                    user_coupon = Coupon(name=f'{user.username}_coupon',shop=None,coupon_type='user',discount=10,code=code,activated=True)
                    user_coupon.save()
                    ##send email to tell user a coupon has  been created for him
                else:
                    if not user_coupon[0].activated:
                        user_coupon[0].activated=True
                        user_coupon[0].save()
                    ## send email to tell user a coupon has been reactivated
            elif len(days_active_in_this_month)<7:
                user_coupon = Coupon.objects.filter(coupon_type='user',name=user.username)
                if user_coupon:
                    if (now - user_coupon[0].created).total_seconds()>week:
                        user_coupon[0].activated=False
                        user_coupon[0].save()
                        ## send email to tell user that coupon is no longer active due to inactivity
            return HttpResponseRedirect(reverse("userdashboard"))
        else:
            return render(request, "users/login2.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('userdashboard'))
        return render(request, "users/login2.html")

def loginview2(request):
    if request.method == "POST":

        # Try to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            userlogins = UserLogin.objects.filter(user=user)
            timestamps = [login.timestamp for login in userlogins]
            minute = 60
            week = 60*60*24*7
            now = datetime.datetime.now(pytz.timezone('Africa/Cairo'))
            timestamps_this_minute = [timestamp for timestamp in timestamps if (now-timestamp).total_seconds()<minute]    
            seconds_active_in_this_minute = set()
            for timestamp in timestamps_this_minute:
                seconds_active_in_this_minute.add(timestamp.second)
            if len(seconds_active_in_this_minute)>=3:
                user_coupon = Coupon.objects.filter(coupon_type='user',name=user.username)
                if not user_coupon and (now-user.date_joined).total_seconds()>week:
                    letters = string.ascii_letters
                    code = ''.join(random.choice(letters) for i in range(5))
                    user_coupon = Coupon(name=user.username,shop=None,coupon_type='user',discount=10,code=code,activated=True)
                    user_coupon.save()
                    ##send email to tell user a coupon has  been created for him
                else:
                    if not user_coupon[0].activated:
                        user_coupon[0].activated=True
                        user_coupon[0].save()
            elif len(seconds_active_in_this_minute)<3:
                user_coupon = Coupon.objects.filter(coupon_type='user',name=user.username)
                if user_coupon:
                    if (now - user_coupon[0].created).total_seconds()>20:
                        user_coupon[0].activated=False
                        user_coupon[0].save()
            return HttpResponseRedirect(reverse("userdashboard"))
        else:
            return render(request, "users/login2.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('userdashboard'))
        return render(request, "users/login2.html")
#for testing

def LogOut(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))
    #request.session['user']=None
    
def SignUp(request):
    if request.method == "POST":
        first = request.POST['first_name']
        last = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        currency = request.POST['Preferred_Currency']
        if currency=='':
            currency='EGP'
        country = request.POST['country']
        code = request.POST['code']
        phone_num = request.POST['phone_num']
        address = request.POST['address']
        # Be sure that password matches confirm_password
        if password != confirm_password:
            return render(request, "users/signup.html", {
                "message": "Your passwords must match."
            })

        # Try to create new user
        try:
            user = User.objects.create_user(first_name=first, last_name=last, username=username, email=email, password=password, preferred_currency=currency,address=address, phone_number=phone_num, phone_number_code=code, country=country)
            user.save()
        except IntegrityError:
            return render(request, "users/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("userdashboard"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('userdashboard'))
        return render(request, "users/signup.html")
@login_required
def changepassword(request):
    if request.method=='POST':
        try:
            old_password = request.POST.get('old_password','')
            new_password = request.POST.get('new_password','')
            confirm_new_password = request.POST.get('confirm_new_password','')
            hash = request.user.password
            if django_pbkdf2_sha256.verify(old_password, hash):
                if new_password==confirm_new_password:
                    user = User.objects.get(username=request.user.username)
                    #user.update(password=new_password)
                    user.set_password(new_password)
                    user.save()
                    user_ = authenticate(request, username=request.user.username, password=new_password)
                    login(request,user_)
                    return render(request,'users/changepassword.html',{'message':"Password changed successfully."})
                else:
                    return render(request,'users/changepassword.html',{'message':"Passwords don't match."})
            else:
                return render(request,'users/changepassword.html',{'message':"Incorrect password."})
        except:
            return render(request,'users/changepassword.html',{'message':"An unexpected error happend, please try again later."})
    else:
        return render(request,"users/changepassword.html")

@login_required        
def orders(request):
    preferred_currency=get_preffered_currency(request)
    currency_ratio=get_currency_ratio(request)
    return render(request,'users/orders.html',{
        'orders':request.user.orders.all(),
        'currency_ratio':currency_ratio,
        'currency_symbol':currency_symbols[preferred_currency]
        })


def discovershops(request):
    return render(request, 'users/discovershops.html', {
        'shops': Shop.objects.all()
    })
@login_required
def create_shop(request):
    if request.method == "GET":
        if not request.user.shop:
            return render(request, "users/StoreName.html")
        else:
            return HttpResponseRedirect(reverse('userdashboard'))
    else:
        shopName = request.POST.get('shopName', '')
        shopAddress = request.POST.get('shopAddress', '')
        shopDesc = request.POST.get('shopDescreption', '')
        if not shopName or not shopAddress or not shopDesc:
            return render(request, "users/StoreName.html",{
                'message':'All fields are required'
            })
        for char in shopName:
            if not char.isalnum() and not char==' ':
                return render(request, "users/StoreName.html",{
                'message':'Shop name must only contain alphanumeric characters and spaces.'
            })
        if not Shop.objects.filter(name=shopName):
            sh = Shop(name=shopName, address=shopAddress, description=shopDesc)
            sh.save()
            u = request.user
            u.shop = sh
            u.is_seller = True
            u.save()
            return HttpResponseRedirect(reverse('shopdashboard'))
        else:
            return render(request, "users/StoreName.html",{
                'message':'This Shop name already Exists'
            })

@login_required
def createtransaction(request):
    products_in_cart=[]
    for product in request.user.cart.all():
        if request.POST[f'{product.id}_quantity']=='0':
            continue
        product_in_cart=InCart(quantity=request.POST[f'{product.id}_quantity'])
        product_in_cart.product = product
        product_in_cart.save()
        products_in_cart.append(product_in_cart)
    if Coupon.objects.filter(code=request.POST['coupon_code']):  
        coupon=Coupon.objects.get(code=request.POST['coupon_code'])
    else:
        coupon=None
    order = Order(bill=round(float(request.POST['total'])/get_currency_ratio(request),2),coupon=coupon)
    order.save()
    for p in products_in_cart:
        order.products.add(p)
    request.user.orders.add(order)
    return HttpResponseRedirect(reverse('checkout', args=[order.id]))

@login_required
def checkout(request,orderid):
    preferred_currency=get_preffered_currency(request)
    currency_ratio=get_currency_ratio(request)
    order = Order.objects.get(id=orderid)
    if order in request.user.orders.all():
        prices = [product.product.price for product in order.products.all()]
        quantities = [product.quantity for product in order.products.all()]
        if order.coupon:
            if order.coupon.coupon_type=='user' or order.coupon.coupon_type=='event':
                products_prices = [(order.products.all()[i],float(prices[i])*quantities[i]*(100-order.coupon.discount)/100) for i in range(len(order.products.all()))]                    
                return render(request,'users/checkout.html',{
                        'order': order,
                        'products_prices': products_prices,
                        'currency_ratio':currency_ratio,
                        'currency_symbol':currency_symbols[preferred_currency]
                    })
            else:
                products_prices = []
                for index,product in enumerate(order.products.all()):
                    if product.product.shop==order.coupon.shop:
                        products_prices.append((product,float(prices[index])*quantities[index]*(100-order.coupon.discount)/100))
                    else:
                        products_prices.append((product,float(prices[index])*quantities[index]))
                return render(request,'users/checkout.html',{
                    'order': order,
                    'products_prices': products_prices,
                    'currency_ratio': currency_ratio,
                    'currency_symbol': currency_symbols[preferred_currency]
                })
        else:
            products_prices=[(order.products.all()[i],float(prices[i])*quantities[i]) for i in range(len(order.products.all()))]
            return render(request,'users/checkout.html',{
                'order': order,
                'products_prices': products_prices,
                'currency_ratio':currency_ratio,
                'currency_symbol':currency_symbols[preferred_currency]
            })
    else:
        return HttpResponseRedirect(reverse('userdashboard'))

@login_required
def finalcheck(request):
    order = Order.objects.get(id=request.POST['order_id'])
    ordered_products = Order.objects.get(id=request.POST['order_id']).products.all()
    for product in ordered_products:
        p = Product.objects.get(name=product.product.name)
        if order not in p.shop.orders.all():
            p.shop.orders.add(order)
        p.remaininginstock = p.remaininginstock - product.quantity
        p.save()
    request.user.cart.clear()    
    order.is_ordered=True
    order.save()

    subject = 'Order has been sent successfully'
    message = f'Hi {request.user.username}, thank you for ordering from our store.'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [request.user.email, ] 
    send_mail( subject, message, email_from, recipient_list )
    

    subject = 'Products from your shop have been ordered'
    message = f'User {request.user.username} has ordered from your shop, check you shop dashboard for order details.'
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = list(set([product.product.shop.user_shop.all()[0].email for product in ordered_products]))
    print(recipient_list)
    send_mail( subject, message, email_from, recipient_list )

    return HttpResponseRedirect(reverse("userdashboard"))

@login_required
def contactus(request):
    if request.method == "GET":
        return render(request,"users/contactus.html")
    else:
        subject=request.POST['subject']
        message=request.POST['message']
        if len(message)<30:
            return render(request,"users/contactus.html",{'message':'Please type a longer message'})
        if  len(subject)<5:
            return render(request,"users/contactus.html",{'message':'Please type a longer subject'})
        email_from = settings.EMAIL_HOST_USER
        superusers = User.objects.filter(is_superuser=True) 
        recipient_list = [user.email for user in superusers]
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect(reverse('userdashboard'))
@login_required
def removefromwishlist(request,productid):
    product=Product.objects.get(id=productid)
    request.user.wishlist.remove(product)
    return HttpResponseRedirect(reverse('wishlist'))
@login_required
def removefromcart(request,productid):
    product=Product.objects.get(id=productid)
    request.user.cart.remove(product)
    return HttpResponseRedirect(reverse('cart'))

def home(request):
    products={}
    displayed={}
    for category in Product.categories:
        products[category[0]] = list(Product.objects.filter(category=category[0]))
        featured = []
        displayed_=[]
        if len(products[category[0]]) <= 6:
            displayed_ = products[category[0]]
        else:
            for p in products[category[0]]:
                if p.featured:
                    featured.append(p)
            if len(featured) == 6:
                displayed_ = featured
            elif len(featured) < 6:
                while len(featured) < 6:
                    random_product = random.choice(products[category[0]])
                    if random_product not in featured:
                        featured.append(random_product)
                displayed_ = featured
            else:
                while len(displayed_) < 6:
                    random_product = random.choice(featured)
                    if random_product not in displayed_:
                        displayed_.append(random_product)
        displayed[category[0]]=displayed_
    return render(request,'users/Mainpage.html',{
        'displayed':displayed,
        'currency_ratio':get_currency_ratio(request),
        'currency_symbol':currency_symbols[get_preffered_currency(request)]
    })