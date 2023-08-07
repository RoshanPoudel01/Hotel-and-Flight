from django.contrib import admin
from hotel.models import Hotel, Image, Phone, Amnities
import csv
from django.http import HttpResponse
# Register your models here.

@admin.register(Amnities)
class AmenitiesAdmin(admin.ModelAdmin):
    list_display=("amenity",)

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ("hotel_name", "email", "city" )
    list_filter = ("city",)
    search_fields = ("hotel_name", "country", "city")
    actions = ["export_as_csv"]
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
@admin.register(Phone)
class PhoneAdmin(admin.ModelAdmin):
    list_display = ("landline", "mobile", "hotel")
    search_fields = ("landline", "mobile", "hotel")
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False
@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("hotel", "image")
    search_fields = ("hotel", "image")
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return False