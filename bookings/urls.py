from django.urls import path
# from .views import CreateBooking
from .views import createBooking,bookingHistory,cancelBooking,book_flight,flightbookingHistory,cancelFlightBooking

app_name = "booking"

urlpatterns = [
    # path("booking/<int:hotelid>", CreateBooking.as_view(), name="create_booking"),
    path("booking/<int:hotelid>", createBooking, name="create_booking"),
    path("booking-history/<int:userid>", bookingHistory, name="booking_history"),
    path("cancel-booking/", cancelBooking, name="cancel_booking"),
     path("book-flight/", book_flight, name="book_flight"),
     path("flight-booking-history/<int:userid>", flightbookingHistory, name="flight_booking_history"),
    path("cancel-flight-booking/", cancelFlightBooking, name="cancel_flight_booking"),

    ]
