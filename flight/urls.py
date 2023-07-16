from django.urls import path
from flight.views import flightpredict,book_flight
app_name = "flight"

urlpatterns = [
    path("flight", flightpredict, name="flight"),
     path("book-flight/", book_flight, name="book_flight"),
]
