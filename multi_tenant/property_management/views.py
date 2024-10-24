from django.shortcuts import redirect, render, get_object_or_404
from .forms import PropertyForm, LeaseForm
from .models import Property, Lease, Review, Listing, Payment

def property_list_view(request):
    properties = Property.objects.filter(is_available=True)
    return render(request, 'property_management/property_list.html', {'properties': properties})

def property_detail_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    reviews = property_instance.reviews.all()
    return render(request, 'property_management/property_detail.html', {'property': property_instance, 'reviews': reviews})

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

def property_update_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        form = PropertyForm(request.POST, instance=property_instance)
        if form.is_valid():
            form.save()  
            return redirect('property_detail', property_id=property_instance.id)
    else:
        form = PropertyForm(instance=property_instance)  
    return render(request, 'property_management/property_form.html', {'form': form, 'property': property_instance})

def property_delete_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    property_instance.delete()
    return redirect('property_list')

def lease_create_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        form = LeaseForm(request.POST)  
        if form.is_valid():
            lease = form.save(commit=False)
            lease.property = property_instance 
            lease.tenant = request.user 
            lease.save()
            return redirect('lease_detail', lease_id=lease.id) 
    else:
        form = LeaseForm()  
    return render(request, 'property_management/lease_form.html', {
        'property': property_instance,
        'form': form  
    })

def lease_detail_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    return render(request, 'property_management/lease_detail.html', {'lease': lease})

def lease_terminate_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    lease.delete()
    return redirect('lease_list')

def review_create_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        pass
    return render(request, 'property_management/review_form.html', {'property': property_instance})

def listing_create_view(request, property_id):
    property_instance = get_object_or_404(Property, id=property_id)
    if request.method == 'POST':
        pass
    return render(request, 'property_management/listing_form.html', {'property': property_instance})

def payment_create_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    if request.method == 'POST':
        pass
    return render(request, 'property_management/payment_form.html', {'lease': lease})
