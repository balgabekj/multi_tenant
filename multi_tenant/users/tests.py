from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

class UserRegistrationTest(TestCase):
    
    def test_user_registration(self):
        url = reverse('register')  # Replace 'register' with your actual URL name
        data = {
            'username': 'testuser',
            'email': 'test@gmail.com',
            'password1': 'Test@1234',
            'password2': 'Test@1234',
            'role': 'tenant',
        }
        response = self.client.post(url, data)
        user = get_user_model().objects.get(username='testuser')
        
        # Check if the user is created
        self.assertEqual(user.username, 'testuser')
        
        # Check if the user is redirected to the login page after registration
        self.assertRedirects(response, reverse('login'))

        # Check if the success message is shown
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(str(messages[0]), "Account created for testuser")

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class UserLoginTest(TestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="Test@1234"
        )
    
    def test_user_login_success(self):
        url = reverse('login')  # Replace 'login' with your actual login URL
        response = self.client.post(url, {'username': 'testuser', 'password': 'Test@1234'})
        
        # Check if the user is logged in and redirected to the correct dashboard
        self.assertRedirects(response, reverse('tenant_dashboard'))  # Adjust based on user role

    def test_user_login_failure(self):
        url = reverse('login')
        response = self.client.post(url, {'username': 'testuser', 'password': 'WrongPassword'})
        
        # Check if the login fails and an error message is shown
        self.assertContains(response, "Invalid username or password.")

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

class DashboardTest(TestCase):
    
    def setUp(self):
        self.tenant_user = get_user_model().objects.create_user(
            username="tenantuser",
            password="Test@1234",
            role="tenant"
        )
        self.renter_user = get_user_model().objects.create_user(
            username="renteruser",
            password="Test@1234",
            role="renter"
        )

    def test_tenant_dashboard(self):
        self.client.login(username="tenantuser", password="Test@1234")
        response = self.client.get(reverse('tenant_dashboard'))  # Adjust the URL if necessary
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/tenant_dashboard.html')

    def test_renter_dashboard(self):
        self.client.login(username="renteruser", password="Test@1234")
        response = self.client.get(reverse('renter_dashboard'))  # Adjust the URL if necessary
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/renter_dashboard.html')

from property_management.models import Property

class ViewRentingPropertyTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='tenantuser', password='testpassword', role='tenant'
        )
        self.property = Property.objects.create(
            title='Test Property', 
            address='123 Main St', 
            rent_price=500.00, 
            available_from='2023-01-01', 
            owner=self.user
        )
        self.user.tenant_profile.rented_property = self.property
        self.user.tenant_profile.save()

    def test_view_rented_property(self):
        self.client.login(username='tenantuser', password='testpassword')
        response = self.client.get(reverse('rented-property'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Property')  # Ensure that the property name appears in the response
        self.assertContains(response, '123 Main St')

