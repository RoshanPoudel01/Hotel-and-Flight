from django.urls import path
from hotel.views import homepage_view, hotel_detail_view, search_view,sort_hotel,termsandconditions

app_name = "hotel"

urlpatterns = [
    path("", homepage_view, name="homepage"),
    path("search/", search_view, name="searchhotel"),
    path("hotel/<int:hotelid>/", hotel_detail_view, name="hotel_detail"),
    path("terms-and-condition",termsandconditions,name="terms"),
    path('sort-hotels/', sort_hotel, name='sort_hotel')
]
