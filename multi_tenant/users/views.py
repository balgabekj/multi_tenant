
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from property_management.models import Lease
from .forms import UserRegisterForm
from users.decorators import tenant_required, renter_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import CustomUser, Tenant
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import timedelta
from django.views.generic import ListView

from django.contrib.auth import login

from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from .models import CustomUser

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            login(request, user)
            user.role = CustomUser.TENANT
            user.save()
            messages.success(request, f'Account created for {username}')
            return redirect('tenant_dashboard')
        else:
            return render(request, 'users/register.html', {'form': form})
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
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect_user_by_role(user)
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'users/login.html')


def redirect_user_by_role(user):
    if user.role == 'tenant':
        return redirect('tenant_dashboard')
    elif user.role == 'renter':
        return redirect('renter_dashboard')

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
        tenant_profile = request.user.tenant_profile
        rented_property = tenant_profile.rented_property if tenant_profile else None
    except CustomUser.tenant_profile.RelatedObjectDoesNotExist:
        rented_property = None 

    return render(request, 'users/view_rented_property.html', {'property': rented_property})


@tenant_required
@login_required
def terminate_rental_agreement(request):
    tenant_profile = request.user.tenant_profile
    if tenant_profile:
        tenant_profile.rented_property = None
        tenant_profile.save()
        return redirect('profile') 

@tenant_required
@login_required
def prolongate_rental_agreement(request):
    tenant_profile = request.user.tenant_profile
    if tenant_profile and tenant_profile.lease_end_date:
        tenant_profile.lease_end_date += timedelta(days=30) 
        tenant_profile.save()
    return redirect('profile')

class UpdatePaymentMethodView(LoginRequiredMixin, UpdateView):
    model = Tenant
    fields = ['payment_method']
    template_name = 'users/update_payment.html'
    success_url = reverse_lazy('profile')

    def get_object(self):
        return self.request.user.tenant_profile



class RenterLeasesView(LoginRequiredMixin, ListView):
    model = Lease
    template_name = 'users/renter_leases.html'
    context_object_name = 'leases'

    def get_queryset(self):
        return self.request.user.renter_profile.lease_history.all()

@login_required
def renew_lease(request, lease_id):
    lease = Lease.objects.get(id=lease_id)
    lease.end_date += timedelta(days=30)  # Extend lease by 30 days
    lease.save()
    return redirect('renter-leases')

@login_required
def terminate_lease(request, lease_id):
    lease = Lease.objects.get(id=lease_id)
    lease.active = False
    lease.save()
    return redirect('renter-leases')

#admin views and models need to be added 