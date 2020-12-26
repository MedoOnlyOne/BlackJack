from django.urls import path
from . import views

urlpatterns = [
    path('<str:shopname>/', views.index, name='shop'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('editproduct/<str:productid>/', views.editproduct, name='editproduct'),
    path('',views.dashboard,name='shopdashboard')
]
