from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
# Create your models here.

class User(AbstractUser):
    # every user will have 3 specified lists (parchases, cart, wishList)
    parchases = models.ManyToManyField(Product, blank=True, related_name="parchases")
    cart = models.ManyToManyField(Product, blank=True, related_name="cart")
    wishList = models.ManyToManyField(Product, blank=True, related_name="wishList")
    pass
