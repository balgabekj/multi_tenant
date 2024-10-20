from django import forms
from .models import Apartment, Lease, Renter

class RenterForm(forms.ModelForm):
    class Meta:
        model = Renter
        fields = ['name', 'phone_number', 'address']

# forms.py
class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ['address', 'price']

# forms.py
class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['tenant', 'apartment', 'start_date', 'end_date', 'rent_amount']


class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['tenant', 'apartment', 'start_date', 'end_date', 'rent_amount']