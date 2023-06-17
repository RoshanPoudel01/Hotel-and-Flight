from django import forms
from .models import Flight
from django.core.exceptions import ValidationError
import datetime
import pytz
utc=pytz.UTC


class FlightForm(forms.ModelForm):
    class Meta:
        model=Flight
        fields=(
           "source",
           "destination",
           "departure_date",
           "arrival_date",
           "airline",
           "stoppage"
        )
        widgets = {
            'departure_date':forms.DateInput(attrs={'type':'datetime-local'}),
            'arrival_date':forms.DateInput(attrs={'type':'datetime-local'}),
        }
    def clean(self):
        cleaned_data = super().clean()
        source = cleaned_data.get("source")
        destination = cleaned_data.get("destination")
        departure_date = cleaned_data.get("departure_date")
        arrival_date = cleaned_data.get("arrival_date")
        if(source==destination):
            raise ValidationError("Source and Destination cannot be same")
        if departure_date < datetime.datetime.now(departure_date.tzinfo):
            raise ValidationError("Departure date cannot be in the past.")
        if arrival_date < datetime.datetime.now(arrival_date.tzinfo):
            raise ValidationError("Arrival date cannot be in the past.")
        if arrival_date <= departure_date:
            raise ValidationError("Departure date cannot be earlier than Arrival date.")
        print(departure_date)
        return cleaned_data
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"   this is used to customize single field
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

