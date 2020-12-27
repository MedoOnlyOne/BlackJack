from django.urls import path
from . import views
# app_name = 'users'
urlpatterns = [
    path('', views.index, name='userdashboard'),
    path('login/', views.LogIn, name='login'),         
    path('loguot/', views.LogOut, name='logout'),       #souq.com/logout/
    path('signup/', views.SignUp, name='signup'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('seller/',views.become_a_seller,name='become_a_seller'),
    path('cart/', views.cart, name='cart'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('orders/',views.orders,name='orders'),
    path('discovershops/', views.discovershops, name="discovershops")
]