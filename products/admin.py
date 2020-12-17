from django.contrib import admin
from .models import Product, Review
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'remaininginstock')
    ordering = ['id']

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'stars')
    ordering = ['id']

# class CartAdmin(admin.ModelAdmin):
#     list_display = ('id', 'products')
#     ordering = ['id']

# class WishlistAdmin(admin.ModelAdmin):
#     list_display = ('id', 'products')
#     ordering = ['id']

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
# admin.site.register(Cart, CartAdmin)
# admin.site.register(Wishlist, WishlistAdmin)