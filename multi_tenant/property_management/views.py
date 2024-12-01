from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import PropertyForm, LeaseForm, ListingForm, PaymentForm, ReviewForm
from .models import Property, Lease, Review, Listing, Payment
from users.decorators import tenant_required, renter_required
from .serializers import LeaseSerializer, LeaseCreateSerializer
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Lease, Property, Tenant
from rest_framework.views import APIView
from django.views.generic import ListView, DetailView


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
    property_instance = get_object_or_404(Property, id=property_id)
    
    if request.method == 'POST':
        form = LeaseForm(request.POST)
        if form.is_valid():
            lease = form.save(commit=False)
            lease.property = property_instance
            lease.tenant = request.user.tenant_profile  # Automatically assign logged-in user as tenant
            lease.save()
            return redirect('lease_detail', lease_id=lease.id)
    else:
        form = LeaseForm()

    return render(request, 'property_management/lease_form.html', {
        'form': form,
        'property': property_instance,
        'properties': Property.objects.all(),
    })


class LeaseListView(ListView):
    model = Lease
    template_name = 'property_management/lease_list.html'
    context_object_name = 'leases'

    def get_queryset(self):
        # You can filter by the user’s tenant profile or other conditions
        return Lease.objects.all()  # Modify as needed


def lease_update_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)

    if request.method == 'POST':
        form = LeaseForm(request.POST, instance=lease)
        if form.is_valid():
            form.save()
            return redirect('lease_detail', lease_id=lease.id)
    else:
        form = LeaseForm(instance=lease)

    return render(request, 'property_management/lease_form.html', {
        'form': form,
        'lease': lease,
    })


class LeaseDetailView(DetailView):
    model = Lease
    template_name = 'property_management/lease_detail.html'
    context_object_name = 'lease'

    def get_object(self, queryset=None):
        # You can add custom logic to ensure the user can only see their own lease or authorized leases
        lease_id = self.kwargs.get('lease_id')
        return get_object_or_404(Lease, id=lease_id)
    


# Lease Terminate View
@login_required
def lease_terminate_view(request, lease_id):
    lease = get_object_or_404(Lease, id=lease_id)
    
    # Check if the user is allowed to terminate the lease
    if request.user != lease.tenant.user and request.user != lease.property.owner:
        return redirect('lease_list')  # or show an error message

    lease.delete()  # Terminate lease
    return redirect('lease_list')  # Redirect to lease list after termination



# Review Views

@renter_required
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


@login_required
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



# REST API FOR LEASE
# class LeaseListCreateAPIView(APIView):
#     def get(self, request):
#         # Retrieve all leases
#         leases = Lease.objects.all()
#         serializer = LeaseSerializer(leases, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         # Create a new lease
#         serializer = LeaseSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=201)
#         return Response(serializer.errors, status=400)
# # Retrieve, update, or delete a lease
# class LeaseDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Lease.objects.all()

#     def get_serializer_class(self):
#         if self.request.method in ['PUT', 'PATCH']:
#             return LeaseCreateSerializer
#         return LeaseSerializer

# # Terminate a lease (custom API endpoint)
# class LeaseTerminateAPIView(APIView):
#     """
#     API to terminate a lease.
#     """

#     def delete(self, request, lease_id):
#         # Fetch the lease object or return 404
#         lease = get_object_or_404(Lease, id=lease_id)

#         # Check permissions
#         if request.user != lease.property.owner and request.user != lease.tenant.user:
#             return Response({"detail": "You are not allowed to terminate this lease."}, status=status.HTTP_403_FORBIDDEN)

#         # Perform the delete operation
#         lease.delete()
#         return Response({"detail": "Lease terminated successfully."}, status=status.HTTP_204_NO_CONTENT)