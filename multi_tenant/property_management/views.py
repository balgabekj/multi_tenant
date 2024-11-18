from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm, LeaseForm, ListingForm, PaymentForm, ReviewForm
from .models import Property, Lease, Review, Listing, Payment
from users.decorators import tenant_required, renter_required

# Property Views

def property_list_view(request):
    properties = Property.objects.filter(is_available=True)
    return render(request, 'property_management/property_list.html', {'properties': properties})


def property_detail_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    reviews = property_instance.reviews.all()
    return render(request, 'property_management/property_detail.html', {
        'property': property_instance, 
        'reviews': reviews
    })

@login_required
def property_create_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = request.user
            property_instance.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'property_management/property_form.html', {'form': form})

@login_required
def property_update_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_instance)
        if form.is_valid():
            form.save()  
            return redirect('property_detail', property_id=property_instance.id)
    else:
        form = PropertyForm(instance=property_instance)  
    return render(request, 'property_management/property_form.html', {
        'form': form, 
        'property': property_instance
    })

@login_required
def property_delete_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.delete()
    return redirect('property_list')

# Lease Views

@tenant_required
def lease_create_view(request, property_id):
    property = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        form = LeaseForm(request.POST)
        if form.is_valid():
            lease = form.save(commit=False)
            lease.property = property  # Attach property to the lease
            lease.save()
            return redirect('lease_detail', lease_id=lease.id)
    else:
        form = LeaseForm()

    return render(request, 'property_management/lease_form.html', {
        'form': form,
        'property': property,
        'properties': Property.objects.all(),
    })

# def lease_update_view(request, lease_id):
#     lease = get_object_or_404(Lease, id=lease_id)
#     property = lease.property

#     if request.method == 'POST':
#         form = LeaseForm(request.POST, instance=lease)
#         if form.is_valid():
#             form.save()
#             return redirect('lease_detail', lease_id=lease.id)
#     else:
#         form = LeaseForm(instance=lease)

#     return render(request, 'property_management/lease_form.html', {
#         'form': form,
#         'lease': lease,
#         'property': property,
#         'properties': Property.objects.all(),
#     })

@login_required
def lease_detail_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    return render(request, 'property_management/lease_detail.html', {'lease': lease})


@login_required
def lease_list_view(request):
    leases = Lease.objects.all()  # You can filter by a specific property if needed
    return render(request, 'property_management/lease_list.html', {
        'leases': leases,
    })


@login_required
def lease_terminate_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    lease.delete()
    return redirect('lease_list')



# Review Views

@tenant_required
def review_create_view(request, property_id):
    print("Review view called")  # Add debug output
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        print("Form data:", form.data)
        if form.is_valid():
            print("Form is valid")
            review = form.save(commit=False)
            review.property = property_instance
            review.tenant = request.user.tenant_profile
            review.save()
            return redirect('property_detail', property_id=property_instance.id)
        else:
            print("Form errors:", form.errors)  # Print form errors for debugging
    else:
        form = ReviewForm()

    return render(request, 'property_management/review_form.html', {
        'property': property_instance,
        'form': form,
    })

# Listing Views

@renter_required
def listing_create_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.property = property_instance
            listing.renter = request.user.renter_profile
            listing.save()
            return redirect('property_detail', property_id=property_instance.id)
    else:
        form = ListingForm()
    return render(request, 'property_management/listing_form.html', {
        'property': property_instance,
        'form': form,
    })

# Payment Views

@tenant_required
def payment_create_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.tenant = request.user.tenant_profile
            payment.lease = lease
            payment.save()
            return redirect('lease_detail', lease_id=lease.id)
    else:
        form = PaymentForm()
    return render(request, 'property_management/payment_form.html', {
        'lease': lease,
        'form': form,
    })
