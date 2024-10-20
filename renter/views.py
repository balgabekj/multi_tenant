from django.shortcuts import render, get_object_or_404, redirect
from .models import Renter, Apartment, Lease
from .forms import ApartmentForm, LeaseForm
from django.utils import timezone
from django.core.mail import send_mail  
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import RenterForm
from .models import Renter


@login_required
def create_renter(request):
    if request.method == 'POST':
        form = RenterForm(request.POST)
        if form.is_valid():
            renter = form.save(commit=False)
            renter.user = request.user  # Link the logged-in user to the renter
            renter.save()
            return redirect('renter_dashboard')  # Adjust this redirect as needed
    else:
        form = RenterForm()
    return render(request, 'renter/create_renter.html', {'form': form})

# Add a new apartment
# views.py
def add_apartment(request, renter_id):
    renter = get_object_or_404(Renter, id=renter_id)
    if request.method == 'POST':
        form = ApartmentForm(request.POST)
        if form.is_valid():
            apartment = form.save(commit=False)
            apartment.renter = renter
            apartment.save()
            return redirect('lease_list')  # Adjust this if you have a different URL for apartments
    else:
        form = ApartmentForm()
    return render(request, 'renter/add_apartment.html', {'form': form})

# View and delete lease details
def view_lease(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    if request.method == 'POST' and 'delete' in request.POST:
        lease.delete()
        return redirect('list_leases', renter_id=lease.apartment.renter.id)
    return render(request, 'renter/lease_details.html', {'lease': lease})

# Lease management (renewals, terminations)
def manage_lease(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    if request.method == 'POST':
        form = LeaseForm(request.POST, instance=lease)
        if form.is_valid():
            form.save()
            return redirect('list_leases', renter_id=lease.apartment.renter.id)
    else:
        form = LeaseForm(instance=lease)
    return render(request, 'renter/manage_lease.html', {'form': form, 'lease': lease})

# View rent due alerts
def view_rent_due_alerts(request, renter_id):
    renter = get_object_or_404(Renter, id=renter_id)
    today = timezone.now().date()
    leases_with_due_rent = Lease.objects.filter(apartment__renter=renter, rent_due_date__lte=today, is_active=True)
    return render(request, 'renter/rent_due_alerts.html', {'renter': renter, 'leases': leases_with_due_rent})

# Post announcements for tenants
def post_announcement(request, renter_id):
    renter = get_object_or_404(Renter, id=renter_id)
    if request.method == 'POST':
        announcement = request.POST.get('announcement')
        # Call function to send announcement to tenants
        send_announcement_to_tenants(renter, announcement)
        return redirect('list_leases', renter_id=renter.id)
    return render(request, 'renter/post_announcement.html')

# Function to send announcement to tenants (via email)
# views.py
def send_announcement_to_tenants(renter, announcement):
    leases = Lease.objects.filter(apartment__renter=renter, is_active=True)
    tenant_emails = [lease.tenant.user.email for lease in leases if lease.tenant.user.email]

    send_mail(
        subject=f"Announcement from {renter.name}",
        message=announcement,
        from_email="noreply@rentalmanagement.com",
        recipient_list=tenant_emails
    )


@login_required
def renter_dashboard(request):
    renter = Renter.objects.get(user=request.user)
    return render(request, 'renter/dashboard.html', {'renter': renter})

@login_required
def create_lease(request):
    if request.method == 'POST':
        form = LeaseForm(request.POST)
        if form.is_valid():
            lease = form.save(commit=False)
            # Optional: Add additional logic, if needed
            lease.save()
            return redirect('lease_list')  # Adjust this to your actual URL name
    else:
        form = LeaseForm()
    return render(request, 'renter/create_lease.html', {'form': form})

@login_required
def lease_list(request):
    # Check if the user is a renter or tenant
    try:
        renter = Renter.objects.get(user=request.user)
        leases = Lease.objects.filter(apartment__renter=renter)
    except Renter.DoesNotExist:
        leases = Lease.objects.filter(tenant__user=request.user)

    return render(request, 'renter/lease_list.html', {'leases': leases})