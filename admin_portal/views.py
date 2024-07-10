from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from accounts.models import CustomUser, BBQBooking
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
@staff_member_required
def admin_dashboard(request):
    total_clients = CustomUser.objects.count()
    total_bookings = BBQBooking.objects.count()
    
    # Upcoming confirmed events (status = 1, date >= today)
    upcoming_events = BBQBooking.objects.filter(
        status=1, 
        date__gte=timezone.now().date()
    ).order_by('date', 'time')[:5]
    
    # New pending events (status = 0)
    new_events = BBQBooking.objects.filter(status=0).order_by('date', 'time')[:5]
    
    context = {
        'total_clients': total_clients,
        'total_bookings': total_bookings,
        'upcoming_events': upcoming_events,
        'new_events': new_events,
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

@staff_member_required
def cancel_booking(request, booking_id):
    booking = BBQBooking.objects.get(id=booking_id)
    booking.status = 2  # Cancelled
    booking.save()
    
    #return successful message as a json response
    return JsonResponse({'message': 'Booking cancelled successfully.'})


