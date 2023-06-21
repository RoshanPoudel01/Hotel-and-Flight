from django.db import models
from bookings.models import Booking
from useraccount.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserPayment(TimeStamp):
    app_user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    # amount=models.CharField(max_length=500)
    # booking_id=models.ForeignKey(Booking, on_delete=models.CASCADE)

@receiver(post_save, sender=User)
def create_user_payment(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(app_user=instance)
