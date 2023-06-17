from django.contrib import admin
from hotel.models import Hotel, Image, Phone, Amnities

# Register your models here.

@admin.register(Amnities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display=("amenity",)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("hotel_name", "email", "city" )
    list_filter = ("city",)
    search_fields = ("hotel_name", "country", "city")



@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("landline", "mobile", "hotel")
    search_fields = ("landline", "mobile", "hotel")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("hotel", "image")
    search_fields = ("hotel", "image")
