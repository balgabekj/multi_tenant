from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Property

class PropertyViewTests(TestCase):

    def setUp(self):
        # Create test users
        self.renter_user = get_user_model().objects.create_user(
            username='renter', password='password123', is_active=True
        )
        self.tenant_user = get_user_model().objects.create_user(
            username='tenant', password='password123', is_active=True
        )

        # Create a test property
        self.property = Property.objects.create(
            title="Test Property",
            address="123 Test St",
            city="Test City",
            state="TS",
            postal_code="12345",
            rent_price=1000.00,
            available_from="2024-12-01",
            is_available=True,
            owner=self.renter_user,
        )

    def test_property_list_view(self):
        response = self.client.get(reverse('property_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Property")

    def test_property_detail_view(self):
        response = self.client.get(reverse('property_detail', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Property")

    def test_property_create_view_renter(self):
        self.client.login(username='renter', password='password123')
        response = self.client.get(reverse('property_create'))
        self.assertEqual(response.status_code, 200)

        # Submit a valid form
        data = {
            'title': 'New Property',
            'address': '456 New St',
            'city': 'New City',
            'state': 'NC',
            'postal_code': '67890',
            'rent_price': '1500.00',
            'available_from': '2024-12-10',
            'is_available': 'True',
        }
        response = self.client.post(reverse('property_create'), data)
        self.assertRedirects(response, reverse('property_list'))
        self.assertTrue(Property.objects.filter(title='New Property').exists())

class LeaseViewTests(TestCase):

    def setUp(self):
        # Create test users
        self.renter_user = get_user_model().objects.create_user(
            username='renter', password='password123', is_active=True
        )
        self.tenant_user = get_user_model().objects.create_user(
            username='tenant', password='password123', is_active=True
        )

        # Create test property
        self.property = Property.objects.create(
            title="Test Property",
            address="123 Test St",
            city="Test City",
            state="TS",
            postal_code="12345",
            rent_price=1000.00,
            available_from="2024-12-01",
            is_available=True,
            owner=self.renter_user,
        )

        # Create tenant and associate with user
        self.tenant_profile = Tenant.objects.create(user=self.tenant_user)

    def test_lease_create_view(self):
        self.client.login(username='tenant', password='password123')
        response = self.client.get(reverse('lease_create', args=[self.property.id]))
        self.assertEqual(response.status_code, 200)

        # Submit a valid form
        data = {
            'lease_start_date': '2024-12-01',
            'lease_end_date': '2025-12-01',
            'rent_amount': '1000.00',
        }
        response = self.client.post(reverse('lease_create', args=[self.property.id]), data)
        self.assertRedirects(response, reverse('lease_detail', args=[1]))  # Assuming lease id is 1

    def test_lease_update_view(self):
        lease = Lease.objects.create(
            property=self.property,
            tenant=self.tenant_profile,
            lease_start_date="2024-12-01",
            lease_end_date="2025-12-01",
            rent_amount=1000.00,
        )
        self.client.login(username='tenant', password='password123')
        response = self.client.get(reverse('lease_update', args=[lease.id]))
        self.assertEqual(response.status_code, 200)

        # Submit a valid form
        data = {'rent_amount': '1200.00'}
        response = self.client.post(reverse('lease_update', args=[lease.id]), data)
        self.assertRedirects(response, reverse('lease_detail', args=[lease.id]))
        lease.refresh_from_db()
        self.assertEqual(lease.rent_amount, 1200.00)

    def test_lease_terminate_view(self):
        lease = Lease.objects.create(
            property=self.property,
            tenant=self.tenant_profile,
            lease_start_date="2024-12-01",
            lease_end_date="2025-12-01",
            rent_amount=1000.00,
        )
        self.client.login(username='tenant', password='password123')
        response = self.client.post(reverse('lease_terminate', args=[lease.id]))
        self.assertRedirects(response, reverse('lease_list'))
        self.assertFalse(Lease.objects.filter(id=lease.id).exists())
