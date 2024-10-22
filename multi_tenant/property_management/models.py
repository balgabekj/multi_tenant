from django.db import models
from multi_tenant.users.models import CustomUser, Tenant, Renter

class Property(models.Model):
    title = models.CharField(max_length=255)  # Property name or title
    address = models.CharField(max_length=255)  # Property address
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per month
    description = models.TextField(blank=True, null=True)
    available_from = models.DateField()  # When the property is available for rent
    is_available = models.BooleanField(default=True)  # Whether the property is currently available
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_properties")  # Renter who owns the property

    def __str__(self):
        return f"{self.title} - {self.city}, {self.state}"

class Lease(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leases')  # Tenant renting the property
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='leases')  # Renter who owns the property
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Monthly rent

    def __str__(self):
        return f"Lease for {self.property.title} (Tenant: {self.tenant.user.username}, Renter: {self.renter.user.username})"

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews')  # Property being reviewed
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='reviews')  # Tenant who is writing the review
    rating = models.PositiveSmallIntegerField()  # Rating out of 5
    comment = models.TextField(blank=True, null=True)  # Optional review comment
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.tenant.user.username} for {self.property.title} - Rating: {self.rating}/5"

class Listing(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='listing')
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='listings')  # Renter who posted the listing
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  # Whether the listing is currently active
    
    def __str__(self):
        return f"Listing: {self.property.title} by {self.renter.user.username}"

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments')  # Tenant making the payment
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='payments')  # Lease for which the payment is made
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)  # e.g., Credit Card, PayPal, Bank Transfer

    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.user.username} on {self.payment_date}"


