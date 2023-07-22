from django.db import models
from useraccount.models import User
from django.core.validators import FileExtensionValidator

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Amnities(TimeStamp):
    amenity=models.CharField(max_length=100)

    def __str__(self):
        return self.amenity
    



class Hotel(TimeStamp):
    hotel_name = models.CharField(max_length=255)
    hotel_description=models.TextField()
    amenities=models.ManyToManyField(Amnities)
    email = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    banner_image=models.ImageField(upload_to="hotelimages")
    price_per_day=models.FloatField()
    added_by=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.hotel_name
    def get_amneties(self):
        amenities_list=[]
        for amenity in self.amenities.all():
            amenities_list.append({'id':amenity.id,'amenity':amenity.amenity})
        return amenities_list

class Image(models.Model):
    image = models.ImageField(upload_to="hotelimages", blank=True, null=True )
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name="hotel_image")
    def __str__(self):
        return self.hotel.hotel_name



class Phone(models.Model):
    landline = models.CharField(max_length=255)
    mobile = models.CharField(max_length=255)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE,related_name="hotel_phone")
    def __str__(self):
        return self.hotel.hotel_name


