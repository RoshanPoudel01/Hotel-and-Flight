from django.contrib import admin
from .models import Flight



@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ("airline", "source", "destination","arrival_date","departure_date","predicted_price" )
    list_filter = ("airline",)
    search_fields = ("airline", "source", "destination")