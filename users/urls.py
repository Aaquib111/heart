from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.authenticate, name ='auth-view'),
    path('redirect/', views.redirectView, name ='redirect-view'),
    path("", views.home, name='home'),
]
