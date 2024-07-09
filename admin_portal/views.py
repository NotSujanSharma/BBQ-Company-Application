from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from accounts.models import CustomUser, BBQBooking
from django.db.models import Count

@staff_member_required
def admin_dashboard(request):
    total_clients = CustomUser.objects.count()
    total_bookings = BBQBooking.objects.count()
    recent_bookings = BBQBooking.objects.order_by('-date')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_bookings': total_bookings,
        'recent_bookings': recent_bookings,
    }
    return render(request, 'dashboard.html', context)

@staff_member_required
def client_list(request):
    clients = CustomUser.objects.annotate(booking_count=Count('bbq_bookings')).order_by('-booking_count', 'date_joined')
    return render(request, 'clients.html', {'clients': clients})

@staff_member_required
def booking_list(request):
    bookings = BBQBooking.objects.all().order_by('-date')
    return render(request, 'bookings.html', {'bookings': bookings})