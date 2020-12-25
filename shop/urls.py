from django.urls import path
from . import views

urlpatterns = [
    path('<str:shopname>/', views.index, name='shop'),
    path('addproduct/', views.addproduct, name='addproduct'),
    path('',views.dashboard,name='shopdashboard')
]
