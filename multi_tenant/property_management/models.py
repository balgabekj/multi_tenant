from django.db import models
from users.models import CustomUser, Tenant, Renter

class Property(models.Model):
    title = models.CharField(max_length=255) 
    address = models.CharField(max_length=255)  
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    rent_price = models.DecimalField(max_digits=10, decimal_places=2) 
    description = models.TextField(blank=True, null=True)
    available_from = models.DateField()  
    is_available = models.BooleanField(default=True)  
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="owned_properties") 

    def __str__(self):
        return f"{self.title} - {self.city}, {self.state}"

class Lease(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='leases')
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leases')  
    lease_start_date = models.DateField()
    lease_end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)  
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Lease for {self.property} (Tenant: {self.tenant})"

class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='reviews') 
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='reviews')  
    rating = models.PositiveSmallIntegerField() 
    comment = models.TextField(blank=True, null=True)  
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.tenant.user.username} for {self.property.title} - Rating: {self.rating}/5"

class Listing(models.Model):
    property = models.OneToOneField(Property, on_delete=models.CASCADE, related_name='listing')
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='listings')  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  
    def __str__(self):
        return f"Listing: {self.property.title} by {self.renter.user.username}"

class Payment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='payments') 
    lease = models.ForeignKey(Lease, on_delete=models.CASCADE, related_name='payments') 
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100)  
    def __str__(self):
        return f"Payment of {self.amount} by {self.tenant.user.username} on {self.payment_date}"


