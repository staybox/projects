from django import forms
from django.core.validators import RegexValidator

class ContactForm(forms.Form):

    client_name = forms.CharField(max_length=25, required=True)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+10001234567'. From 9 to 15 digits allowed.")
    phone_number = forms.CharField(validators=[phone_regex], max_length=15, required=True)
    order = forms.CharField(max_length=200, required=True)
