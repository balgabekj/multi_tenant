from rest_framework import serializers
from .models import Lease, Property, Tenant, Review

class LeaseSerializer(serializers.ModelSerializer):
    property = serializers.StringRelatedField(read_only=True)  # Display property title
    tenant = serializers.StringRelatedField(read_only=True)    # Display tenant username

    class Meta:
        model = Lease
        fields = '__all__'

class LeaseCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lease
        fields = ['property', 'tenant', 'lease_start_date', 'lease_end_date', 'rent_amount']

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'property', 'tenant', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'property', 'tenant', 'created_at']