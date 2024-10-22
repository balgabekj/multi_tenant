from urllib import request

from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import UserRegisterForm
from users.decorators import tenant_required, renter_required
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .models import CustomUser
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            return redirect('login')
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
    fields = ['first_name', 'last_name', 'email']  # Add other fields as needed
    template_name = 'users/profile.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        # Return the currently logged-in user
        return self.request.user

