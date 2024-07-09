from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_home'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('clients/', views.client_list, name='admin_client_list'),
    path('bookings/', views.booking_list, name='admin_booking_list'),
]