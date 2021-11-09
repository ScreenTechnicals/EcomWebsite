from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('contactlist/', views.contactlist, name="contactlist"),
    path('contactlist/<str:id>/', views.contact_view, name="contact_view"),
    path('order/<str:id>/', views.order_view, name="order_view"),
    path('dashboard/search/', views.search_order, name="search_order"),
]
