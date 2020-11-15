from django.contrib import admin
from .models import User, Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'remaininginstock')
    ordering = ['id']

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    ordering = ['-is_staff']

admin.site.register(User, UserAdmin)
admin.site.register(Product, ProductAdmin)