from django import forms
from .models import Property, Lease, Review, Listing, Payment

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'address', 'city', 'state', 'postal_code', 'rent_price', 'description', 'available_from', 'is_available']

class LeaseForm(forms.ModelForm):
    class Meta:
        model = Lease
        fields = ['tenant', 'lease_start_date', 'lease_end_date', 'rent_amount']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['tenant', 'rating', 'comment']

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['property']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'payment_method']
