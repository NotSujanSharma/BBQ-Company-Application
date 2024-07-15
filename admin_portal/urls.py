from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_home'),
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('clients/', views.client_list, name='admin_client_list'),
    path('add-client/', views.add_client, name='admin_add_client'),

    path('client-details/<int:client_id>/', views.client_details, name='admin_client_details'),
    path('edit-client/<int:client_id>/', views.edit_client, name='admin_edit_client'),
    path('delete-client/<int:client_id>/', views.delete_client, name='admin_delete_client'),

    path('bookings/', views.booking_list, name='admin_booking_list'),
    path('marketing/', views.marketing, name='admin_marketing' ),

    path('add-booking/', views.add_booking, name='admin_add_booking'),

    path('confirm-booking/<int:booking_id>/', views.confirm_booking, name='admin_confirm_booking'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='admin_cancel_booking'),
    path('complete-event/<int:booking_id>/', views.complete_event, name='admin_complete_event'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='admin_delete_booking'),
    path('edit-booking/<int:booking_id>/', views.edit_booking, name='admin_edit_booking'),
    path('get-booking-details/<int:booking_id>/', views.get_booking_details, name='admin_get_booking_details'),

    path('create_campaign/', views.create_campaign, name='admin_create_campaign'),
    path('import_subscribers/', views.import_subscribers, name='admin_import_subscribers'),
    path('export_subscribers/', views.export_subscribers, name='admin_export_subscribers'),
    path('subscriber_management/', views.subscriber_management, name='admin_subscriber_management'),
    path('campaign_details/<int:campaign_id>/', views.campaign_details, name='campaign_details'),
    path('campaigns/', views.campaigns, name='admin_campaigns'),


    path('analytics/', views.analytics, name='admin_analytics'),

    path('api/analytics/', views.analytics_api, name='analytics_api'),

    path('calendar/', views.calendar_view, name='admin_calendar'),
    path('api/calendar-events/', views.get_calendar_events, name='calendar_events'),


    path('staff-overview/', views.staff_overview, name='admin_staff_overview'),
    path('staff-list/', views.staff_list, name='admin_staff_list'),
    path('add-staff/', views.add_staff, name='admin_add_staff'),
    path('edit-staff/<int:staff_id>/', views.edit_staff, name='admin_edit_staff'),
    path('delete-staff/<int:staff_id>/', views.delete_staff, name='admin_delete_staff'),

    # update_attendance
    path('update-attendance/', views.update_attendance, name='update_attendance'),

]