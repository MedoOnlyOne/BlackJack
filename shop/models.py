from django.db import models
from products.models import Product

class Shop(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(max_length=100)
    products = models.ManyToManyField(Product, blank=True, related_name="products")

    def __str__(self):
        return f"{self.name}"