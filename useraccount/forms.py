from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django import forms

User = get_user_model()


class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r"^[a-zA-Z]+$")],
        error_messages={"invalid": "Name can only contain alphabets a-z or A-Z"},
    )
    last_name = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r"^[a-zA-Z]+$")],
        error_messages={"invalid": "Name can only contain alphabets a-z or A-Z"},
    )
    phone = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r"^[0-9]+$")],
        error_messages={"invalid": "Phone Number can only be Numbers 0-9"},
    )
    email = forms.CharField(
        max_length=100,
        error_messages={"invalid": "Invalid Email! Please insert a valid Email"},
    )
    address = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r"^[a-zA-Z0-9_.-]*$")],
        error_messages={"invalid": "Please insert a valid Address"},
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "address",
            "phone",
            "image",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"   this is used to customize single field
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
class PasswordChangeForm(forms.ModelForm):
    class Meta:
        model=User
        fields = ("__all__")
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"   this is used to customize single field
            for visible in self.visible_fields():
                visible.field.widget.attrs["class"] = "form-control"



class UserEditForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r"^[a-zA-Z]+$")],
        error_messages={"invalid": "Name can only contain alphabets a-z or A-Z"},
    )
    last_name = forms.CharField(
        max_length=50,
        validators=[RegexValidator(r"^[a-zA-Z]+$")],
        error_messages={"invalid": "Name can only contain alphabets a-z or A-Z"},
    )
    phone = forms.CharField(
        max_length=100,
        validators=[RegexValidator(r"^[0-9]+$")],
        error_messages={"invalid": "Phone Number can only be Numbers 0-9"},
    )
    email = forms.CharField(
        max_length=100,
        error_messages={"invalid": "Invalid Email! Please insert a valid Email"},
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "email",
            "username",
            "address",
            "phone",
            "image",
        )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].widget.attrs["class"] = "form-control"   this is used to customize single field
        for visible in self.visible_fields():
            visible.field.widget.attrs["class"] = "form-control"
