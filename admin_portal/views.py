from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404
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
        # date__gte=timezone.now().date() //// need to uncomment this line
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
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        }, status=405)

    try:
        booking = get_object_or_404(BBQBooking, id=booking_id)
        
        if booking.status == 2:
            return JsonResponse({
                'success': False,
                'message': 'Booking is already cancelled'
            }, status=400)
        
        if booking.status == 3:
            return JsonResponse({
                'success': False,
                'message': 'Cannot cancel a completed booking'
            }, status=400)
        
        booking.status = 2  # Cancelled
        booking.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Booking successfully cancelled'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

@staff_member_required
def complete_event(request, booking_id):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        }, status=405)

    try:
        booking = get_object_or_404(BBQBooking, id=booking_id)
        
        if booking.status == 3:
            return JsonResponse({
                'success': False,
                'message': 'Event is already marked as completed'
            }, status=400)
        
        if booking.status == 2:
            return JsonResponse({
                'success': False,
                'message': 'Cannot complete a cancelled booking'
            }, status=400)
        
        booking.status = 3  # Completed
        booking.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Event marked as completed'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

@staff_member_required
def delete_booking(request, booking_id):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        }, status=405)

    try:
        booking = get_object_or_404(BBQBooking, id=booking_id)
        booking.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Booking successfully deleted'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)

@staff_member_required
def confirm_booking(request, booking_id):
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'message': 'Invalid request method'
        }, status=405)

    try:
        booking = get_object_or_404(BBQBooking, id=booking_id)
        
        if booking.status == 1:
            return JsonResponse({
                'success': False,
                'message': 'Booking is already confirmed'
            }, status=400)
        
        if booking.status == 2:
            return JsonResponse({
                'success': False,
                'message': 'Cannot confirm a cancelled booking'
            }, status=400)
        
        if booking.status == 3:
            return JsonResponse({
                'success': False,
                'message': 'Event already completed'
            }, status=400)
        
        booking.status = 1  # Confirmed
        booking.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Booking successfully confirmed'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'An error occurred: {str(e)}'
        }, status=500)