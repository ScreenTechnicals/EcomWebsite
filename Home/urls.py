from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="home"),
    path('orders/', views.orders, name="orders"),
    path('menu/', views.menu, name="menu"),
    path('accounts/signup/', views.signup, name="signup"),
    path('accounts/login/', views.login, name="login"),
    path('accounts/logout/', views.logout, name="logout"),
    path('profile/', views.profile, name="profile"),
]

