from django.db import models

# Create your models here.
class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Stoppage(models.TextChoices):
    NOSTOPPAGE = 0, "Nostoppage"
    ONE = 1, "1 Stop"
    TWO = 2, "2 Stop"
    THREE = 3, "3 Stop"
class Cities(models.TextChoices):  
    SELECT="select","Select City"
    DELHI = "delhi", "Delhi"
    BANGALORE = "bangalore", "Bangalore"
    NEWDELHI = "newdelhi", "New Delhi"
    KOLKATA = "kolkata", "Kolkata"
    MUMBAI = "mumbai", "Mumbai"
    COCHIN = "cochin", "Cochin"
    CHENNAI = "chennai", "Chennai"  
    HYDERABAD = "hyderabad", "Hyderabad"  


class Airline(models.TextChoices):
    SELECT="select","Select Airline"
    JETAIRWAYS = "jetairways", "Jet Airways"
    INDIGO = "indigo", "IndiGo"
    AIRINDIA = "airindia", "Air India"
    MULTIPLECARRIERS = "multiplecarriers", "Multiple carriers"
    SPICEJET = "spicejet", "SpiceJet"
    VISTARA = "vistara", "Vistara"
    AIRASIA = "airasia", "Air Asia"
    GOAIR = "goair", "GoAir"
    MULTIPLECARRIERSPREMIUMECONOMY = "multiplecarrierspremiumeconomy", "Multiple carriers Premium economy"
    JETAIRWAYSBUSINESS = "jetairwaysbusiness", "Jet Airways Business"
    VISTARAPREMIUMECONOMY = "vistarapremiumeconomy", "Vistara Premium economy"
    TRUJET = "trujet", "Trujet"

class Flight(TimeStamp):
    destination=models.CharField(max_length=255,choices=Cities.choices,default=Cities.SELECT)
    airline=models.CharField(max_length=255,choices=Airline.choices,default=Airline.SELECT)
    source=models.CharField(max_length=255,choices=Cities.choices,default=Cities.SELECT)
    arrival_date=models.DateTimeField()
    departure_date=models.DateTimeField()
    stoppage= models.CharField(
        max_length=100,
        choices=Stoppage.choices,
        default=Stoppage.NOSTOPPAGE,
    )
    predicted_price=models.CharField(null=True,blank=True)

