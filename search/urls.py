from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_paginated, name='search'),
    path('a/',views.search,name='search_paginated')
]