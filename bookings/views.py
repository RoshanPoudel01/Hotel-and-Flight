from django.shortcuts import render, get_object_or_404, redirect
from .forms import BookingForm
from useraccount.models import User
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from hotel.models import Hotel
from .models import Booking
import stripe
from django.http import JsonResponse
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
            print("hereqsdjvaskhd")
            booking.save()
            return redirect(checkout_session.url, code=303)
    else:
        booking_form = BookingForm()
    return render(request, "make_booking.html", {"form": booking_form, "hotel": hotel})


login_required


def bookingHistory(request, userid):
    bookinghistory = Booking.objects.filter(user_id=userid)
    print(bookinghistory)

    return render(request, "booking_history.html", {"booking": bookinghistory})