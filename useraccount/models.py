from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="userimages", blank=True, null=True)
    stripe_session=models.CharField(max_length=500,null=True,blank=True)
    is_client = models.BooleanField(default=False)
    stripe_customer_id=models.CharField(max_length=500,null=True,blank=True)
