from django import forms
from hotel.models import Hotel, Phone, Image


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

    # def clean_price_per_day(self):
    #     price_per_day = self.cleaned_data.get("price_per_day")
    #     print(price_per_day)
    #     if price_per_day <= 0:
    #         raise forms.ValidationError("Price can not be less than zero.")
    #     return price_per_day


class ImageForm(forms.ModelForm):
  
    class Meta:
        model = Image
        exclude = ("hotel","image",)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"

    # def clean_price_per_day(self):
    #     price_per_day = self.cleaned_data.get("price_per_day")
    #     print(price_per_day)
    #     if price_per_day <= 0:
    #         raise forms.ValidationError("Price can not be less than zero.")
    #     return price_per_day
