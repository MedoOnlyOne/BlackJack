from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    description = models.TextField()
    remaininginstock = models.PositiveSmallIntegerField(default=1)
    def __str__(self):
        return '%s' %self.name

class User(AbstractUser):
    # every user will have 3 specified lists (parchases, cart, wishList)
    parchases = models.ManyToManyField(Product, blank=True, related_name="parchases")
    cart = models.ManyToManyField(Product, blank=True, related_name="cart")
    wishList = models.ManyToManyField(Product, blank=True, related_name="wishList")

