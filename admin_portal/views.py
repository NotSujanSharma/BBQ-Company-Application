from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, get_object_or_404, redirect
from accounts.models import CustomUser, BBQBooking
from django.db.models import Count
from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse
from accounts.forms import BBQBookingForm
from .forms import CampaignForm
from .models import Campaign
from datetime import timedelta

from django.db.models import Avg

# import messages
from django.contrib import messages

@staff_member_required
def admin_dashboard(request):
    total_clients = CustomUser.objects.count()
    total_bookings = BBQBooking.objects.count()
    current_month = timezone.now().month
    current_year = timezone.now().year
    new_clients_this_month = CustomUser.objects.filter(
        date_joined__month=current_month,
        date_joined__year=current_year
    ).count()
    # Upcoming confirmed events (status = 1, date >= today)
    upcoming_events = BBQBooking.objects.filter(
        status=1, 
        # date__gte=timezone.now().date() //// need to uncomment this line
    ).order_by('date', 'time')[:5]
    
    # New pending events (status = 0)
    new_events = BBQBooking.objects.filter(status=0).order_by('date', 'time')[:5]
    
    context = {
        'total_clients': total_clients,
        'new_clients_this_month': new_clients_this_month,
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

@staff_member_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(BBQBooking, id=booking_id)
    
    # Ensure the user owns this booking
    
    if request.method == 'POST':
        if booking.status == 3:
            messages.error(request, "You can't edit a booking that is already completed.")
            return redirect(reverse('admin_booking_list'))
        form = BBQBookingForm(request.POST, instance=booking)
        if form.is_valid():
            
            booking = form.save(commit=False)
            booking.user = request.user
            booking.drinks = form.cleaned_data['guests']
            booking.event_type = form.cleaned_data['event_type']
            # Process main dishes
            main_dishes = {}
            for dish in form.MAIN_DISHES:
                dish_key = f'main_dish_{dish[0]}'
                count_key = f'main_dish_{dish[0]}_count'
                if dish_key in request.POST and request.POST.get(count_key):
                    main_dishes[dish[0]] = int(request.POST.get(count_key))
            booking.main_dishes = main_dishes

            # Process side dishes
            side_dishes = {}
            for dish in form.SIDE_DISHES:
                dish_key = f'side_dish_{dish[0]}'
                count_key = f'side_dish_{dish[0]}_count'
                if dish_key in request.POST and request.POST.get(count_key):
                    side_dishes[dish[0]] = int(request.POST.get(count_key))
            booking.side_dishes = side_dishes

            # Process desserts
            desserts = {}
            for dessert in form.DESSERTS:
                dessert_key = f'dessert_{dessert[0]}'
                count_key = f'dessert_{dessert[0]}_count'
                if dessert_key in request.POST and request.POST.get(count_key):
                    desserts[dessert[0]] = int(request.POST.get(count_key))
            booking.desserts = desserts

            booking.save()
            return redirect(reverse('admin_dashboard'))
    else:
        form = BBQBookingForm(instance=booking)
    
    return render(request, 'admin_edit_booking.html', {'form': form, 'booking': booking})

@staff_member_required
def marketing(request):
    recent_campaigns = Campaign.objects.order_by('-date_sent')[:5]
    avg_open_rate = Campaign.objects.aggregate(Avg('open_rate'))['open_rate__avg']
    avg_click_rate = Campaign.objects.aggregate(Avg('click_rate'))['click_rate__avg']
    context = {
        'recent_campaigns': recent_campaigns,
        'avg_open_rate': avg_open_rate,
        'avg_click_rate': avg_click_rate,
    }
    return render(request, 'marketing/marketing.html',context)




@staff_member_required
def import_subscribers(request):
    return render(request, 'marketing/import_subscribers.html')

@staff_member_required
def export_subscribers(request):
    return render(request, 'marketing/export_subscribers.html')

@staff_member_required
def create_campaign(request):
    if request.method == 'POST':
        form = CampaignForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.user = request.user
            campaign.save()
            messages.success(request, 'Campaign created successfully')
            return redirect('admin_marketing')
        else:
            messages.error(request, 'An error occurred. Please try again.')

    return render(request, 'marketing/create_campaign.html', {'form': CampaignForm()})

@staff_member_required
def campaign_details(request, campaign_id):
    campaign = Campaign.objects.get(id=campaign_id)
    return render(request, 'marketing/campaign_details.html', {'campaign': campaign})


@staff_member_required
def subscriber_management(request):
    return render(request, 'marketing/subscriber_management.html')

@staff_member_required
def campaigns(request):
    campaigns = Campaign.objects.all()
    return render(request, 'marketing/campaigns.html', {'campaigns': campaigns})


@staff_member_required
def analytics(request):
    return render(request, 'analytics.html')

@staff_member_required
def analytics_api(request):
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)

    # Bookings over time
    bookings_over_time = BBQBooking.objects.filter(date__range=[start_date, end_date]) \
        .values('date') \
        .annotate(count=Count('id')) \
        .order_by('date')

    # Event types distribution
    event_types_distribution = BBQBooking.objects.values('event_type') \
        .annotate(count=Count('id')) \
        .order_by('-count')

    # Top 5 locations
    top_locations = BBQBooking.objects.values('location') \
        .annotate(count=Count('id')) \
        .order_by('-count')[:5]

    # Total bookings
    total_bookings = BBQBooking.objects.count()

    # Average guests per booking
    average_guests = BBQBooking.objects.aggregate(Avg('guests'))['guests__avg']

    # Most popular event type
    most_popular_event_type = event_types_distribution.first()['event_type']

    # Recent bookings
    recent_bookings = BBQBooking.objects.order_by('-date')[:10].values('date', 'event_type', 'guests', 'status')

    data = {
        'bookings_over_time': list(bookings_over_time),
        'event_types_distribution': list(event_types_distribution),
        'top_locations': list(top_locations),
        'total_bookings': total_bookings,
        'average_guests': average_guests,
        'most_popular_event_type': most_popular_event_type,
        'recent_bookings': list(recent_bookings),
    }

    return JsonResponse(data)


@staff_member_required
def calendar_view(request):
    return render(request, 'calendar.html')

@staff_member_required
def get_calendar_events(request):
    bookings = BBQBooking.objects.filter(status=1)
    events = []
    for booking in bookings:
        events.append({
            'id': booking.id,
            'title': f"{booking.get_event_type_display()}",
            'start': f"{booking.date}T{booking.time}",
            'extendedProps': {
                'time': booking.time.strftime('%H:%M')
            }
        })
    return JsonResponse(events, safe=False)

@staff_member_required
def get_booking_details(request, booking_id):
    booking = get_object_or_404(BBQBooking, id=booking_id)
    
    data = {
        'success': True,
        'booking': {
            'id': booking.id,
            'event_type': booking.get_event_type_display(),
            'date': booking.date.strftime('%Y-%m-%d'),
            'time': booking.time.strftime('%H:%M'),
            'location': booking.location,
            'guests': booking.guests,
            'status': booking.status,
            'main_dishes': booking.main_dishes,
            'side_dishes': booking.side_dishes,
            'desserts': booking.desserts,
            'drinks': booking.drinks,
            'user': {
                'first_name': booking.user.first_name,
                'last_name': booking.user.last_name,
                'email': booking.user.email,
                'contact_number': booking.user.contact_number,
            }
        }
    }
    
    return JsonResponse(data)
