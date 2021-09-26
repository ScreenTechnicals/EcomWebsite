from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('orders/', views.orders, name="orders"),
    path('menu/', views.menu, name="menu"),
]

