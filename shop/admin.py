from django.contrib import admin
from .models import Shop, Coupon
# Register your models here.

class ShopAdmin(admin.ModelAdmin):
    list_display = ('id','name')
    ordering = ['id']

class CouponAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'discount', 'activated')
    ordering = ['id']

admin.site.register(Shop, ShopAdmin)
admin.site.register(Coupon, CouponAdmin)
