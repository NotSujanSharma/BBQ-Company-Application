from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm, LoginForm, UserProfileForm, BBQBookingForm
from django.views.decorators.http import require_GET 
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseForbidden, JsonResponse
from django.contrib import messages
from .models import BBQBooking


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "You have been successfully signed up.")
            return redirect('profile')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                return redirect('profile')  # Redirect to profile page after login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect to profile page after update
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('login')

@login_required
def view_booked_events(request):
    # Get all bookings for the current user, ordered by date
    bookings = BBQBooking.objects.filter(user=request.user).order_by('date', 'time')
    
    return render(request, 'booked_events.html', {'bookings': bookings})

@login_required
def book_bbq(request):
    if request.method == 'POST':
        form = BBQBookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.drinks = form.cleaned_data['guests']
            booking.status = 0  # Reset status to pending
            booking.event_type = form.cleaned_data['event_type']
            # Process main dishes
            main_dishes = {}

            for dish in form.MAIN_DISHES:
                if form.cleaned_data[f'main_dish_{dish[0]}']:
                    main_dishes[dish[0]] = form.cleaned_data[f'main_dish_{dish[0]}_count']
                    print("main dishes:")
                    print(main_dishes)
            booking.main_dishes = main_dishes

            # Process side dishes
            side_dishes = {}
            for dish in form.SIDE_DISHES:
                if form.cleaned_data[f'side_dish_{dish[0]}']:
                    side_dishes[dish[0]] = form.cleaned_data[f'side_dish_{dish[0]}_count']
            booking.side_dishes = side_dishes

            # Process desserts
            desserts = {}
            for dessert in form.DESSERTS:
                if form.cleaned_data[f'dessert_{dessert[0]}']:
                    desserts[dessert[0]] = form.cleaned_data[f'dessert_{dessert[0]}_count']
            booking.desserts = desserts

            booking.save()
            return redirect('view_booked_events')  # You'll need to create this view
    else:
        form = BBQBookingForm()
    return render(request, 'book_bbq.html', {'form': form})

@login_required
def delete_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(BBQBooking, id=booking_id)
        
        # Ensure the user owns this booking
        if booking.user != request.user:
            return HttpResponseForbidden("You don't have permission to delete this booking.")
        
        
        # Delete the booking
        if booking.status == 2:

            booking.delete()
        else:
            messages.error(request, "You can't delete a booking that is not cancelled.")

            return redirect(reverse('view_booked_events'))

            

        
        # Redirect back to the list of bookings
        return redirect(reverse('view_booked_events'))
    
    # If it's not a POST request, redirect to the list of bookings
    return redirect(reverse('view_booked_events'))

@login_required
def cancel_booking(request, booking_id):
    if request.method == 'POST':
        booking = get_object_or_404(BBQBooking, id=booking_id)
        
        # Ensure the user owns this booking
        if booking.user != request.user:
            return HttpResponseForbidden("You don't have permission to cancel this booking.")
        
        # Cancel the booking
        if booking.status == 3:
            messages.error(request, "You can't cancel a booking that is already completed.")
            return redirect(reverse('view_booked_events'))

        if booking.status == 1:
            messages.error(request, "This booking is already confirmed. Please contact us to cancel this booking.")
            return redirect(reverse('view_booked_events'))
        booking.status = 2
        booking.save()
        
        messages.success(request, "Booking cancelled successfully.")

        # Redirect back to the list of bookings
        return redirect(reverse('view_booked_events'))

@login_required
def edit_booking(request, booking_id):
    booking = get_object_or_404(BBQBooking, id=booking_id)
    
    # Ensure the user owns this booking
    if booking.user != request.user:
        return HttpResponseForbidden("You don't have permission to edit this booking.")
    
    if request.method == 'POST':
        if booking.status == 3:
            messages.error(request, "You can't edit a booking that is already completed.")
            return redirect(reverse('view_booked_events'))
        if booking.status==1:
            messages.error(request, "Booking is already confirmed, Please contact us to edit this booking")
            return redirect(reverse('view_booked_events'))

        form = BBQBookingForm(request.POST, instance=booking)
        if form.is_valid():
            
            booking = form.save(commit=False)
            booking.user = request.user
            booking.status = 0  # Reset status to pending
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
            return redirect(reverse('view_booked_events'))
    else:
        form = BBQBookingForm(instance=booking)
    
    return render(request, 'edit_booking.html', {'form': form, 'booking': booking})

@require_GET
def get_booking_details(request, booking_id):
    try:
        booking = BBQBooking.objects.select_related('user').get(id=booking_id)
        data = {
            'success': True,
            'booking': {
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
    except BBQBooking.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Booking not found'}, status=404)

