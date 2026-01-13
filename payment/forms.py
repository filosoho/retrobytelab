from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import ShippingAddress


# Registration form
class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = [
            "full_name",
            "email",
            "address1",
            "address2",
            "city",
            "state",
            "zipcode",
        ]
        exclude = [
            "user",
        ]
