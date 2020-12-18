from django.db import models
import datetime
import uuid
# Create your models here.

class Review(models.Model):
    text = models.TextField()
    stars = models.DecimalField(max_digits=7,decimal_places=2)
    user = models.ForeignKey('users.User',on_delete=models.CASCADE,null=True)
    date = models.DateTimeField(auto_now=True, blank=True)
    def __str__(self):
        return f'{self.text}'


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    description = models.TextField(blank=True)
    remaininginstock = models.PositiveSmallIntegerField(default=1)
    featured = models.BooleanField(default=False)
    image = models.ImageField(null=True,blank=True,upload_to='product_images/')
    shop = models.ForeignKey('shop.Shop',on_delete=models.CASCADE)
    reviews = models.ManyToManyField(Review, blank=True, related_name="reviews")
    def __str__(self):
        return f'{self.name}'
    def __unicode__(self):
        return self.id

# class Cart(models.Model):
#     products = models.ManyToManyField(Product, blank=True, related_name="purchased_product")

#     def __str__(self):
#         return f'{self.products}'

# class Wishlist(models.Model):
#     products = models.ManyToManyField(Product, blank=True, related_name="wished_product")

#     def __str__(self):
#         return f'{self.products}'
