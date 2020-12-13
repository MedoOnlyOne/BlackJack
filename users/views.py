from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required #@login_required(login_url='login/')
from django.core import serializers
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import User, Product
# Create your views here.

@login_required(login_url='login/')
def index(request):
    if request.method == "POST":
        first = request.POST.get("first", "")
        last = request.POST.get("last", "")
        code = request.POST.get("code", "")
        num = request.POST.get("num", "")
        email = request.POST.get("email", "")
        password = request.POST.get("password", "")
        currency = request.POST.get("currency", "")
        
        user = User.objects.filter(username=request.user.username)
        user.update(first_name=first, last_name=last, phone_number=num, phone_number_code=code, password=password, email=email, preferred_currency=currency)

        return HttpResponseRedirect(reverse("index"))

    else:
        # get user's wishList, cart and parchases
        wishList = request.user.wishList.all()
        cart = request.user.cart.all()
        parchases = request.user.parchases.all()
        shops = request.user.shops.all()
        
        first_name = request.user.first_name
        last_name = request.user.last_name
        num = request.user.phone_number
        code = request.user.phone_number_code
        email = request.user.email
        password = request.user.password
        currency = request.user.preferred_currency

        return render(request, 'users/Dashboard.html', {
            'wishList': wishList,
            'cart': cart,
            'parchases': parchases,
            'shops':shops,
            'first': first_name,
            'last': last_name,
            'num': num,
            'code': code,
            'email': email,
            'password':password,
            'currency':currency,
            'currency_list': ["EGP","EUR","USD","GBP"]
        })

def LogIn(request):
    if request.method == "POST":
    
        # Try to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "users/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, "users/login.html")

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
        country = request.POST['country']
        code = request.POST['code']
        phone_num = request.POST['phone_num']
        # Be sure that password matches confirm_password
        if password != confirm_password:
            return render(request, "users/signup.html", {
                "message": "Your passwords must match."
            })

        # Try to create new user
        try:
            user = User.objects.create_user(first_name=first, last_name=last, username=username, email=email, password=password, preferred_currency=currency, phone_number=phone_num, phone_number_code=code, country=country)
            user.save()
        except IntegrityError:
            return render(request, "users/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return render(request, "users/signup.html")

    
  


