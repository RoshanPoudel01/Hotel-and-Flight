from django.urls import path
from .views import clientdashboard, add_hotel, add_phone, add_images,list_hotel,edit_hotel,delete_hotel,list_image,list_phone,delete_image,delete_phone,list_bookings,export_bookings,export_hotels


app_name = "client"
urlpatterns = [
    path("client-dashboard/", clientdashboard, name="clientdashboard"),
    path("addhotel/", add_hotel, name="add_hotel"),
    path("listhotel", list_hotel, name="list_hotel"),
    path("edithotel/<int:hotelid>/", edit_hotel, name="edit_hotel"),
    path("deletehotel/", delete_hotel, name="delete_hotel"),
    path("addphone/<int:hotelid>/", add_phone, name="add_phone"),
    path("listphone/", list_phone, name="list_phone"),
    path("addimages/<int:hotelid>/", add_images, name="add_image"),
    path("listimages/", list_image, name="list_image"),
    path("deleteimage/", delete_image, name="delete_image"),
    path("deletephone/", delete_phone, name="delete_phone"),
    path("listbookings/", list_bookings, name="list_bookings"),
    path("exportbookings/", export_bookings, name="export_bookings"),
    path("exporthotels/", export_hotels, name="export_hotels"),
    

]