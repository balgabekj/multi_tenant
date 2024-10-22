from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    TENANT = 'tenant'
    RENTER = 'renter'
    ADMIN = 'admin'
    
    ROLE_CHOICES = [
        (TENANT, 'Tenant'),
        (RENTER, 'Renter'),
        (ADMIN, 'Admin'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=TENANT)

    def is_tenant(self):
        return self.role == self.TENANT

    def is_renter(self):
        return self.role == self.RENTER

    def is_admin(self):
        return self.role == self.ADMIN

class Tenant(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="tenant_profile")
    rented_property = models.ForeignKey('Property', on_delete=models.SET_NULL, null=True, blank=True)
    lease_start_date = models.DateField(null=True, blank=True)
    lease_end_date = models.DateField(null=True, blank=True)
    payment_method = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Tenant: {self.user.username}, Property: {self.rented_property}'

class Renter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="renter_profile")
    watched_properties = models.ManyToManyField('Property', blank=True)  # Properties they have viewed or are interested in
    lease_history = models.ManyToManyField('Lease', blank=True)  # Past or active leases
    current_property = models.ForeignKey('Property', on_delete=models.SET_NULL, null=True, blank=True, related_name="current_property")

    def __str__(self):
        return f'Renter: {self.user.username}'

    