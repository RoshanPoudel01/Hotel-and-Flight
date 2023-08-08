from django import forms
from hotel.models import Hotel, Phone, Image
from django.core.exceptions import ValidationError


class HotelCreationForm(forms.ModelForm):
    class Meta:
        model = Hotel
        exclude = ("added_by",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    def clean_price_per_day(self):
        price_per_day = self.cleaned_data.get("price_per_day")
        print(price_per_day)
        if price_per_day <= 0:
            raise forms.ValidationError("Price can not be less than zero.")
        return price_per_day


class PhoneForm(forms.ModelForm):
    class Meta:
        model = Phone
        exclude = ("hotel",)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"



# ALLOWED_FILE_FORMATS = ['jpeg', 'jpg', 'png', 'gif']

class ImageForm(forms.ModelForm):
  
    class Meta:
        model = Image
        exclude = ("hotel",)
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
  
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    # def clean_image(self):
    #     image = self.files.getlist('image')
    #     if image:
    #         file_extension = image.name.split('.')[-1].lower()
    #         if file_extension not in ALLOWED_FILE_FORMATS:
    #             raise ValidationError(f"Unsupported file format. Only {', '.join(ALLOWED_FILE_FORMATS)} are allowed.")
    #     return image
    
