from django.urls import path
from . import views

urlpatterns = [
    path('addcoupon/', views.addcoupon, name='addcoupon'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('deactivatecoupon/<str:couponid>', views.deactivatecoupon, name='deactivatecoupon'),
    path('editproduct/<str:productid>/', views.editproduct, name='editproduct'),
    path('',views.dashboard,name='shopdashboard'),
    path('<str:shopname>/', views.index, name='shop'),
    path('activecoupons/', views.activecoupons,name='activecoupons'),
    path('orders/',views.orders,name='shop_orders'),
    path('remove/<str:productid>',views.removefromshop,name='removefromshop')
]
