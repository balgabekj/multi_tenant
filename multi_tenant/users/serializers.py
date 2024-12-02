from rest_framework import serializers
from .models import CustomUser, Tenant, Renter

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'role']

class TenantSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Tenant
        fields = ['user', 'rented_property', 'lease_start_date', 'lease_end_date', 'payment_method']

class RenterSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()

    class Meta:
        model = Renter
        fields = ['user', 'watched_properties', 'lease_history', 'current_property']
