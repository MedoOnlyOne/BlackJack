from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:productname>/', views.product, name='product')
]