from django.db import models
from useraccount.models import User
from hotel.models import Hotel
from django.db.models.functions import Now

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

BOOL_CHOICES = ((True, 'Booked'), (False, 'Cancelled'))

class Booking(TimeStamp):
    check_in_date=models.DateField()
    check_out_date=models.DateField()
    amount=models.FloatField()
    user=models.ForeignKey(User ,
        on_delete=models.CASCADE)
    hotel=models.ForeignKey(Hotel,on_delete=models.CASCADE)
    status = models.BooleanField(choices=BOOL_CHOICES,default=True)
    transaction_id = models.CharField(max_length=500, null=True, blank=True)


    def __str__(self):
        return self.hotel.hotel_name
    
    def duration(self):
        return ((self.check_out_date - self.check_in_date).days)+1