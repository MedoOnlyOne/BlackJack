from django.urls import path
from . import views

urlpatterns = [
    path('<str:productid>/', views.product, name='productpage')
    ]