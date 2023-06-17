from django.urls import path
from hotel.views import homepage_view, hotel_detail_view, search_view, add_hotel,add_phone,add_images

app_name = "hotel"

urlpatterns = [
    path("", homepage_view, name="homepage"),
    path("search/", search_view, name="searchhotel"),
    path("hotel/<int:hotelid>/", hotel_detail_view, name="hotel_detail"),
    path("addhotel/", add_hotel, name="add_hotel"),
    path("addphone", add_phone, name="add_phone"),
    path("addimages", add_images, name="add_images"),

]
