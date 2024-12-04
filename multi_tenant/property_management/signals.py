from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Tenant

@receiver(post_save, sender=CustomUser)
def create_tenant_profile(sender, instance, created, **kwargs):
    # Check if the user was just created and is a tenant
    if created and instance.role == CustomUser.TENANT:
        Tenant.objects.get_or_create(user=instance)
