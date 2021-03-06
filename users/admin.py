from django.contrib import admin
from .models import User, Product,Order,InCart,UserLogin
# import user_visit
# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff')
    ordering = ['-is_staff']

class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('user' , 'timestamp')
    ordering = ['timestamp']

admin.site.register(User, UserAdmin)
admin.site.register(Order)
admin.site.register(InCart)
admin.site.register(UserLogin,UserLoginAdmin)