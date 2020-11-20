from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=7,decimal_places=2)
    description = models.TextField()
    remaininginstock = models.PositiveSmallIntegerField(default=1)
    featured = models.BooleanField(default=False)
    image = models.ImageField(null=True,upload_to='product_images/')
    def __str__(self):
        return '%s' %self.name
