from django.db import models
from products.models import Product

class Shop(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    address = models.TextField(max_length=100,)
    products = models.ManyToManyField(Product, blank=True, related_name="products")
    coupons = models.ManyToManyField('shop.Coupon',blank=True,default=None,related_name='shop_coupons')
    orders = models.ManyToManyField('users.Order',blank=True,default=None,related_name='shop_orders')
    featured = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.name}"

class Coupon(models.Model):
    name = models.CharField(max_length=30)
    code = models.CharField(max_length=25,unique=True)
    activated = models.BooleanField()
    discount = models.PositiveSmallIntegerField()
    shop = models.ForeignKey('shop.Shop',on_delete=models.CASCADE,null=True,blank=True)
    created = models.DateTimeField(auto_now=True)
    coupon_types = [('shop','shop'),('event','event'),('user','user')]
    coupon_type = models.CharField(max_length=5,choices=coupon_types,default='shop')
    def is_user_coupon(self):
        return self.coupon_type == 'user'
    def is_event_coupon(self):
        return self.coupon_type == 'event'
    def __str__(self):
        return f"{self.name}"