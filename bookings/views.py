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


# Create your views here.

# class CreateBooking(CreateView):
#     model = Booking
#     form_class = BookingForm
#     template_name = "make_booking.html"
#     success_url= reverse_lazy("hotels:homepage")
#     def form_valid(self, form):
#         # This method is called when valid form data has been POSTed.
#         # It should return an HttpResponse.
#         form.save()
#         return super().form_valid(form)


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
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
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
                mode="payment",
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


login_required


def bookingHistory(request, userid):
    today = date.today()
    bookinghistory = Booking.objects.filter(user_id=userid, check_in_date__lt=today,status=True)
    upcomingbookings = Booking.objects.filter(user_id=userid, check_in_date__gt=today, status=True)
    return render(request, "booking_history.html", {"booking": bookinghistory,"upcomingbookings":upcomingbookings})



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