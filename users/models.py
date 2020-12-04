from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
from shop.models import Shop
# Create your models here.

class User(AbstractUser):
    # every user will have 3 specified lists (parchases, cart, wishList)
    parchases = models.ManyToManyField(Product, blank=True, related_name="Purchases")
    cart = models.ManyToManyField(Product, blank=True, related_name="Cart")
    wishList = models.ManyToManyField(Product, blank=True, related_name="WishList")
    shops = models.ManyToManyField(Shop,blank=True, related_name="OwnedShops")
