from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_home'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('clients/', views.client_list, name='admin_client_list'),
    path('bookings/', views.booking_list, name='admin_booking_list'),
    path('confirm-booking/<int:booking_id>/', views.confirm_booking, name='admin_confirm_booking'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='admin_cancel_booking'),
    path('complete-event/<int:booking_id>/', views.complete_event, name='admin_complete_event'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='admin_delete_booking'),
]