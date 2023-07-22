from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookingForm
from payment.models import UserPayment
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from hotel.models import Hotel
from .models import Booking
import stripe
from datetime import date
from django.conf import settings
from flight.models import Flight
from bookings.models import FlightBooking
import math 



# Create your views here.


@login_required
def createBooking(request, hotelid):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    hotel = get_object_or_404(Hotel, id=hotelid)
    if request.method == "POST":
        booking_form = BookingForm(request.POST)
        if booking_form.is_valid():
            booking = booking_form.save(commit=False)
            booking.hotel_id = hotel.id
            booking.user_id = request.user.id
            booking.amount = booking.duration() * hotel.price_per_day
            fee=booking.amount * 0.25
            print( hotel.added_by.id)
            checkout_session=stripe.checkout.Session.create(
                mode="payment",
                 line_items=[
                    {
                        "price_data": {
                            "currency": "usd",
                            "unit_amount": int(booking.amount) * 100,
                            "product_data": {
                                "name": "Hotel booking",
                            },
                        },
                        "quantity": 1,
                    },
                ],
                payment_intent_data={
                    "application_fee_amount":  int(fee)*100,
                     "transfer_data": {"destination": hotel.added_by.stripe_customer_id},
                        },
                        customer_creation="always",
                success_url=settings.REDIRECT_DOMAIN
                + "/payment_successful?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=settings.REDIRECT_DOMAIN + "/payment_cancelled",
                )
            
            booking.transaction_id = checkout_session.id
            booking.status = False
            booking.save()
            return redirect(checkout_session.url, code=303)
    else:
        booking_form = BookingForm()
    return render(request, "make_booking.html", {"form": booking_form, "hotel": hotel})


@login_required
def bookingHistory(request, userid):
    today = date.today()
    bookinghistory = Booking.objects.filter(user_id=userid, check_in_date__lt=today,status=True)
    upcomingbookings = Booking.objects.filter(user_id=userid, check_in_date__gte=today, status=True)
    return render(request, "booking_history.html", {"booking": bookinghistory,"upcomingbookings":upcomingbookings})


@login_required
def cancelBooking(request):
    bookingid=request.POST.get("bookingid")
    booking=Booking.objects.get(id=bookingid)
    payment=UserPayment.objects.get(stripe_checkout_id=booking.transaction_id)
    booking.status=False
    final_amount=booking.amount-booking.amount*0.8
    booking.amount=final_amount
    payment.amount=final_amount
    booking.save()
    payment.save()
    return redirect(reverse("booking:booking_history", args=(request.user.id,)))


@login_required
def book_flight(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        flight_id = int(request.POST.get('flightid'))
        predicted_price = float(request.POST.get('price'))
        flight=Flight.objects.get(id=flight_id)
      
        checkout_session=stripe.checkout.Session.create(
            mode="payment",
             line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": math.floor(predicted_price)*100,
                        "product_data": {
                            "name": "Flight booking",
                        },
                    },
                    "quantity": 1,
                },
            ],
            customer_creation="always",
            success_url=settings.REDIRECT_DOMAIN
            + "/payment_successful_flight?session_id={CHECKOUT_SESSION_ID}",
            cancel_url=settings.REDIRECT_DOMAIN + "/payment_cancelled",
            )
        book_flight=FlightBooking.objects.create(flight=flight, user_id=request.user.id, amount=predicted_price, status=False,transaction_id=checkout_session.id)
        book_flight.save()
        return redirect(checkout_session.url, code=303)
            
    return render(request, 'book.html')
    


@login_required
def flightbookingHistory(request, userid):
    today = date.today()
    bookinghistory = FlightBooking.objects.filter(user_id=userid,status=True)
    upcomingbookings = FlightBooking.objects.filter(user_id=userid,status=True)
    # upcomingbookings = FlightBooking.objects.filter(user_id=userid, check_in_date__gte=today, status=True)
    return render(request, "flight_bookings.html", {"booking": bookinghistory,"upcomingbookings":upcomingbookings})

@login_required
def cancelFlightBooking(request):
    bookingid=request.POST.get("bookingid")
    booking=FlightBooking.objects.get(id=bookingid)
    payment=UserPayment.objects.get(stripe_checkout_id=booking.transaction_id)
    booking.status=False
    final_amount=booking.amount-booking.amount*0.8
    booking.amount=final_amount
    payment.amount=final_amount
    booking.save()
    payment.save()
    return redirect(reverse("booking:booking_history", args=(request.user.id,)))
