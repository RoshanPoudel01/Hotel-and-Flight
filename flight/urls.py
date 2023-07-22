from django.urls import path
from flight.views import flightpredict
app_name = "flight"

urlpatterns = [
    path("flight", flightpredict, name="flight"),
  
]
