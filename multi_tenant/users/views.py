from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from property_management.models import Lease, Property
from .forms import UserRegisterForm
from users.decorators import tenant_required, renter_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import CustomUser, Tenant, Renter
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.views.generic import ListView
from property_management.models import Property



def home(request):
    properties = Property.objects.all()[:2]  
    return render(request, 'users/home.html', {'properties': properties})

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data.get('role')  # Сохраняем роль
            user.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')  # После регистрации перенаправьте на login
        else:
            print(form.errors)  # Debugging: печать ошибок
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

def user_login(request: HttpRequest):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect_user_by_role(user)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')

def redirect_user_by_role(user):
    if user.role == 'tenant':
        return redirect('tenant_dashboard')
    elif user.role == 'renter':
        return redirect('renter_dashboard')
    else:
        return redirect('home')

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')

@tenant_required
def tenant_dashboard(request):
    return render(request, 'users/tenant_dashboard.html')

@renter_required
def renter_dashboard(request):
    return render(request, 'users/renter_dashboard.html')

class UserProfileView(LoginRequiredMixin, UpdateView):   
    model = CustomUser
    fields = ['first_name', 'last_name', 'email']
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

@tenant_required
@login_required
def view_renting_property(request):
    try:
        tenant_profile = request.user.tenant_profile  # Get the tenant profile related to the user
        rented_property = tenant_profile.rented_property if tenant_profile else None
    except CustomUser.tenant_profile.RelatedObjectDoesNotExist:
        rented_property = None  # If tenant_profile does not exist for the user, set rented_property to None

    return render(request, 'users/view_rented_property.html', {'property': rented_property})


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def terminate_rental_agreement(request):
    user = request.user
    try:
        tenant_profile = user.tenant_profile
        if tenant_profile:
            tenant_profile.rented_property = None
            tenant_profile.save()
            return Response({"message": "Rental agreement terminated successfully."}, status=200)
        return Response({"error": "No tenant profile found."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import logging

logger = logging.getLogger('users')

class ProlongateRentalAgreementView(APIView):
    
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tenant_profile = request.user.tenant_profile  # Ensure the user has a tenant profile
            if tenant_profile and tenant_profile.lease_end_date:
                tenant_profile.lease_end_date += timedelta(days=30)  # Extend lease by 30 days
                tenant_profile.save()
                return Response({"message": "Rental agreement prolonged by 30 days."}, status=HTTP_200_OK)
            return Response({"error": "No lease to prolong."}, status=HTTP_400_BAD_REQUEST)
        except AttributeError:
            return Response({"error": "User does not have a tenant profile."}, status=HTTP_400_BAD_REQUEST)


class UpdatePaymentMethodAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            tenant_profile = request.user.tenant_profile  # Ensure the user has a tenant profile
            payment_method = request.data.get('payment_method')
            if not payment_method:
                return Response({"error": "Payment method is required."}, status=HTTP_400_BAD_REQUEST)
            tenant_profile.payment_method = payment_method
            tenant_profile.save()
            return Response({"message": "Payment method updated successfully."}, status=HTTP_200_OK)
        except AttributeError:
            return Response({"error": "User does not have a tenant profile."}, status=HTTP_400_BAD_REQUEST)
        

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from property_management.models import Lease
@method_decorator(login_required, name='dispatch')
class RenterLeasesView(TemplateView):
    template_name = "users/renter_leases.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            tenant_profile = self.request.user.tenant_profile
            context['leases'] = Lease.objects.filter(tenant=tenant_profile)
        except AttributeError:
            context['leases'] = []  # If tenant_profile is not found, provide an empty list
        return context
@login_required
def renew_lease(request, lease_id):
    lease = Lease.objects.get(id=lease_id)
    lease.lease_end_date += timedelta(days=30)  # Extend lease by 30 days
    lease.save()
    return redirect('renter-leases')




@login_required
def terminate_lease(request, lease_id):
    try:
        # Fetch the lease related to the tenant or property they are associated with
        lease = Lease.objects.get(id=lease_id, tenant=request.user.renter_profile)
        lease.is_active = False  # Mark the lease as inactive
        lease.save()
        messages.success(request, "Lease terminated successfully!")
    except Lease.DoesNotExist:
        messages.error(request, "Lease not found or you do not have permission to terminate it.")
    return redirect('renter-leases')

#admin views and models need to be added 

@login_required
@renter_required
def view_my_property(request):
    # Fetch properties owned by the logged-in user
    user_properties = Property.objects.filter(owner=request.user)

    return render(request, 'users/my_properties.html', {
        'properties': user_properties
    })

