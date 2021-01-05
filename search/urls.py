from django.urls import path
from . import views

urlpatterns = [
    path('', views.search, name='search'),
    path('a/',views.search_paginated,name='search_paginated')
]