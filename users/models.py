from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
from shop.models import Shop
# Create your models here.

class User(AbstractUser):
    # every user will have 3 specified lists (parchases, cart, wishList)
    phone_number=models.CharField(max_length=15,null=False,default="")
    phone_number_code=models.CharField(max_length=4,null=False,default="+20")
    country=models.CharField(max_length=30,null=False,default="Egypt")
    preferred_currency=models.CharField(max_length=3,null=False,default="EGP")
    address = models.CharField(max_length=100,null=False,default="")
    is_seller = models.BooleanField(default=False)
    parchases = models.ManyToManyField(Product, blank=True, related_name="Purchases")
    cart = models.ManyToManyField(Product, blank=True, related_name="Cart")
    wishList = models.ManyToManyField(Product, blank=True, related_name="WishList")
    shops = models.ManyToManyField(Shop,blank=True, related_name="OwnedShops")
   