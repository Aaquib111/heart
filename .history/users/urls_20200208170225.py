from django.contrib import admin
from django.urls import path
from . import views
from .views import ChartData

urlpatterns = [
    path('', views.home, name ='home-view'),
    path('auth/', views.authenticate, name ='auth-view'),
    path('redirect/', views.redirectView, name ='redirect-view'),
    path('api/chart/data/', ChartData.as_view(), name='data-view'),
]
