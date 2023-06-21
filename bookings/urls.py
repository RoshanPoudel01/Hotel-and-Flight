from django.urls import path
# from .views import CreateBooking
from .views import createBooking,bookingHistory,cancelBooking

app_name = "booking"

urlpatterns = [
    # path("booking/<int:hotelid>", CreateBooking.as_view(), name="create_booking"),
    path("booking/<int:hotelid>", createBooking, name="create_booking"),
    path("booking-history/<int:userid>", bookingHistory, name="booking_history"),
    path("cancel-booking/<int:bookingid>", cancelBooking, name="cancel_booking"),

    ]
