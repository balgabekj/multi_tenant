# renter/models.py
from django.db import models
from django.contrib.auth.models import User

class Renter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Apartment(models.Model):
    renter = models.ForeignKey(Renter, on_delete=models.CASCADE, related_name='apartments')
    address = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.address

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.user.username

class Lease(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='leases')
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, related_name='leases')
    start_date = models.DateField()
    end_date = models.DateField()
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    rent_due_date = models.DateField(null=True, blank=True)  # Optional rent due date
    is_active = models.BooleanField(default=True)  # Active lease flag

    def __str__(self):
        return f"Lease for {self.apartment} by {self.tenant}"
