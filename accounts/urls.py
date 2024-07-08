from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.user_logout, name='logout'),
    path('book-bbq/', views.book_bbq, name='book_bbq'),
    path('my-bookings/', views.view_booked_events, name='view_booked_events'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('edit-booking/<int:booking_id>/', views.edit_booking, name='edit_booking'),
]