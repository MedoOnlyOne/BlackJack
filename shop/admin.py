from django.contrib import admin
from .models import Shop
# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    ordering = ['id']

admin.site.register(Shop, ShopAdmin)
