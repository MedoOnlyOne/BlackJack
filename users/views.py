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
    
    # get user's wishList, cart and parchases
    wishList = request.user.wishList.all()
    cart = request.user.cart.all()
    parchases = request.user.parchases.all()
    shops = request.user.shops.all()
    return render(request, 'users/index.html', {
        'wishList': wishList,
        'cart': cart,
        'parchases': parchases,
        'shops':shops
    })
    #return render(request, 'users/index.html',{'user':request.user})

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

    # """if request.method== 'POST':
    #     username=request.POST['username']
    #     password=request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user:
    #         login(request, user)
    #       #  request.session['user']=serializers.serialize('json',User.objects.all())
    #         return render(request,'users/index.html',{'username':username,'email':user.email,'first':user.first_name,'last':user.last_name,'user':user})
    #     else:
    #         #request.session['user']=None
    #         return render(request,'users/login.html',{'message':'Incorrect Username or password','user':request.session.get('user',None)})
    # if request.user.is_authenticated:
    #    return render(request,'users/index.html',{'username':request.user.username,'email':request.user.email,'first':request.user.first_name,'last':request.user.last_name,'user':request.user}) 
    # return render(request,'users/login.html',{'user':request.session.get('user',None)})"""



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

        # Be sure that password matches confirm_password
        if password != confirm_password:
            return render(request, "users/signup.html", {
                "message": "Your passwords must match."
            })

        # Try to create new user
        try:
            user = User.objects.create_user(first_name=first, last_name=last, username=username, email=email, password=password)
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

    
    # """if request.method == 'POST':
    #     first = request.POST['first_name']
    #     last = request.POST['last_name']
    #     username = request.POST['username']
    #     email = request.POST['email']
    #     password = request.POST['password']
    #     confirm_password = request.POST['confirm_password']

    #     if password == confirm_password:
    #         #try:
    #         user = User.objects.create_user(first_name=first, last_name=last, username=username, email=email, password=password)
    #         user.save()
        
    #         return render(request, 'users/index.html', {
    #             'first': first,
    #             'last': last,
    #             'email': email,
    #             'username': username
    #         })
    #         except:
    #             return render(request, 'users/signup.html')
        
    #     else:
    #         return render(request, 'users/signup.html', {
    #             'message': "password didn't match",'user':user
    #         })"""


