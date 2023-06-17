from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date


class BookingForm(forms.ModelForm):
    class Meta:
        model=Booking
        # fields="__all__"
        fields=(
           "check_in_date",
           "check_out_date",
           
        )
        widgets = {
            
            'check_in_date':forms.DateInput(attrs={'type':'date'}),
            'check_out_date':forms.DateInput(attrs={'type':'date'})
        }
    def clean(self):
        cleaned_data = super().clean()
        check_in_date = cleaned_data.get('check_in_date')
        check_out_date = cleaned_data.get('check_out_date')

        if not check_in_date or not check_out_date:
            # Don't proceed with further validation if either date is missing
            return cleaned_data

        today = date.today()
        if check_in_date < today:
            raise ValidationError("Check-in date cannot be in the past.")
        if check_out_date < today:
            raise ValidationError("Check-out date cannot be in the past.")
        if check_out_date <= check_in_date:
            raise ValidationError("Check-out date cannot be earlier than check-in date.")

        return cleaned_data
    
    # def clean_check_in_date(self):
    #     check_in_date = self.cleaned_data.get('check_in_date')
    #     check_out_date = self.cleaned_data.get('check_out_date')
    #     today = date.today()
    #     if check_in_date < today:
    #         raise ValidationError('Check-in date cannot be a past date.')
    #     print(check_in_date)
    #     print(check_out_date)
    #     if check_out_date < timezone.now().date():
    #         raise ValidationError('Check-out date cannot be a past date.')
      
    #     return check_in_date,check_out_date

    # def clean_check_out_date(self):
    #     check_in_date = self.cleaned_data.get('check_in_date')
    #     check_out_date = self.cleaned_data.get('check_out_date')
    #     print(check_in_date)
    #     print(check_out_date)
    #     if check_out_date < timezone.now().date():
    #         raise ValidationError('Check-out date cannot be a past date.')
    #     if check_out_date <= check_in_date:
    #         raise ValidationError('Check-out date must be after check-in date.')
    #     return check_out_date
    
    
   

    