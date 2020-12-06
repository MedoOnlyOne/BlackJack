from django.urls import path
from . import views

urlpatterns = [
    path('<str:shopname>/', views.index, name='shopdashboard'),
    path('<str:shopname>/addproduct', views.addproduct, name='addproduct')
]
