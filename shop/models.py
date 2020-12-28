from django.db import models
from products.models import Product

class Shop(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    address = models.TextField(max_length=100,)
    products = models.ManyToManyField(Product, blank=True, related_name="products")
    coupons = models.ManyToManyField('shop.Coupon',default=None,related_name='shop_coupons')
    def __str__(self):
        return f"{self.name}"

class Coupon(models.Model):
    name=models.CharField(max_length=30)
    code=models.CharField(max_length=25)
    activated=models.BooleanField()
    discount=models.PositiveSmallIntegerField()
    shop = models.ForeignKey('shop.Shop',on_delete=models.CASCADE,null=True)
    def __str__(self):
        return f"{self.name}"