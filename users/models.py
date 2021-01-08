from django.db import models
from django.contrib.auth.models import AbstractUser
from products.models import Product
from shop.models import Shop
import uuid
from django.contrib.auth import user_logged_in
from django.dispatch import receiver
import datetime
import pytz
# Create your models here.

class User(AbstractUser):
    # every user will have 3 specified lists (parchases, cart, wishList)
    phone_number = models.CharField(max_length=15,null=False,default="")
    phone_number_code = models.CharField(max_length=4,null=False,default="+20")
    country = models.CharField(max_length=30,null=False,default="Egypt")
    preferred_currency = models.CharField(max_length=3,null=False,default="EGP")
    address = models.CharField(max_length=100,null=False,default="")
    is_seller = models.BooleanField(default=False)
    cart = models.ManyToManyField('products.Product', blank=True, related_name="cart")
    wishlist = models.ManyToManyField('products.Product', blank=True, related_name="wishlist" )
    shop = models.ForeignKey('shop.Shop', related_name="user_shop",on_delete=models.SET_NULL, null=True, blank=True, default=None)
    orders = models.ManyToManyField('users.Order', blank=True, related_name="user_orders")
    def __str__(self):
        return f'{self.username}'


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # user=models.ForeignKey('users.User',on_delete=models.PROTECT, blank=True, null=True)
    products = models.ManyToManyField('users.InCart', related_name="ordered_products")
    is_delivered = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)       
    bill = models.FloatField(default=0.0)
    coupon = models.ForeignKey('shop.Coupon',on_delete=models.SET_NULL,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['created']
    def __str__(self):
        return f'{self.id}'

class InCart(models.Model):
    product = models.ForeignKey('products.Product',on_delete=models.CASCADE,null=True,default=None)
    quantity = models.PositiveSmallIntegerField(default=1)

class UserLogin(models.Model):
    user = models.ForeignKey('users.User',related_name='user_login',on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)


@receiver(user_logged_in)
def create_user_login(sender,request,user,**kwargs):
    u = UserLogin(user=user)
    u.save()


