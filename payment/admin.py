from django.contrib import admin
from .models import UserPayment


# Register your models here.
@admin.register(UserPayment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("app_user", "payment_bool", "stripe_checkout_id", "created_at")
