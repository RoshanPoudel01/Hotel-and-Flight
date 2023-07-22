from django import forms
from .models import Hotel, Phone, Image
from django.core.exceptions import ValidationError
from PIL import Image as PILImage
from io import BytesIO
# class PriceFilterFormHelper(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_method = 'get'
#         layout_fields = []
#         for field_name, field in self.fields.items():
#             if isinstance(field, RangeField):
#                 layout_field = Field(field_name, template="slider/fields/range_slider.html")
#             else:
#                 layout_field = Field(field_name)
#             layout_fields.append(layout_field)
#         layout_fields.append(StrictButton("Submit", name='submit', type='submit', css_class='btn btn-fill-out btn-block mt-1'))
#         self.helper.layout = Layout(*layout_fields)

class PriceRangeForm(forms.Form):
    min_price = forms.DecimalField(label='Minimum Price')
    max_price = forms.DecimalField(label='Maximum Price')

    def clean_min_price(self):
        min_price = self.cleaned_data.get("min_price")
        if min_price < 0:
            raise forms.ValidationError("Price can not be less than zero.")
        return min_price
    def clean_max_price(self):
        max_price = self.cleaned_data.get("max_price")
        if max_price < 0:
            raise forms.ValidationError("Price can not be less than zero.")
        return max_price
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
        fields = "__all__"

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

ALLOWED_FILE_FORMATS = ['jpeg', 'jpg', 'png', 'gif']
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
    def clean_image(self):
        image = self.files.getlist('image')
        if image:
            file_extension = image.name.split('.')[-1].lower()
            if file_extension not in ALLOWED_FILE_FORMATS:
                raise ValidationError(f"Unsupported file format. Only {', '.join(ALLOWED_FILE_FORMATS)} are allowed.")
        return image
    