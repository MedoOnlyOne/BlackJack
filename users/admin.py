from django.contrib import admin
from .models import User, Product
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'remaininginstock')
    ordering = ['id']

admin.site.register(User)
admin.site.register(Product, ProductAdmin)