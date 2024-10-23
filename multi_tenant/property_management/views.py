from django.shortcuts import redirect, render, get_object_or_404
from .forms import PropertyForm, LeaseForm
from .models import Property, Lease, Review, Listing, Payment

# Property List View
def property_list_view(request):
    properties = Property.objects.filter(is_available=True)
    return render(request, 'property_management/property_list.html', {'properties': properties})

# Property Detail View
def property_detail_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    reviews = property_instance.reviews.all()
    return render(request, 'property_management/property_detail.html', {'property': property_instance, 'reviews': reviews})

# Property Create View
def property_create_view(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST)
        if form.is_valid():
            property_instance = form.save(commit=False)
            property_instance.owner = request.user  # Assuming the user is logged in
            property_instance.save()
            return redirect('property_list')
    else:
        form = PropertyForm()
    return render(request, 'property_management/property_form.html', {'form': form})

# Property Update View
def property_update_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_instance)  # Bind the form with the existing instance
        if form.is_valid():
            form.save()  # Save the updated property
            return redirect('property_detail', property_id=property_instance.id)
    else:
        form = PropertyForm(instance=property_instance)  # Pre-populate the form with the property data
    return render(request, 'property_management/property_form.html', {'form': form, 'property': property_instance})

# Property Delete View
def property_delete_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.delete()
    return redirect('property_list')

# Lease Create View
def lease_create_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        form = LeaseForm(request.POST)  # Initialize the form with POST data
        if form.is_valid():
            lease = form.save(commit=False)
            lease.property = property_instance  # Associate the lease with the property
            lease.tenant = request.user  # Assuming the user is a tenant
            lease.save()
            return redirect('lease_detail', lease_id=lease.id)  # Redirect to the lease detail page
    else:
        form = LeaseForm()  # Initialize an empty form for GET requests

    return render(request, 'property_management/lease_form.html', {
        'property': property_instance,
        'form': form  # Pass the form to the template
    })



# Lease Detail View
def lease_detail_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    return render(request, 'property_management/lease_detail.html', {'lease': lease})

# Lease Terminate View
def lease_terminate_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    lease.delete()  # or set a status to inactive
    return redirect('lease_list')

# Review Create View
def review_create_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        # Logic to create a new review
        pass
    return render(request, 'property_management/review_form.html', {'property': property_instance})

# Listing Create View
def listing_create_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        # Logic to create a new listing
        pass
    return render(request, 'property_management/listing_form.html', {'property': property_instance})

# Payment Create View
def payment_create_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    if request.method == 'POST':
        # Logic to create a new payment
        pass
    return render(request, 'property_management/payment_form.html', {'lease': lease})
