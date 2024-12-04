from django.urls import path
from .views import (
    property_list_view,
    property_detail_view,
    property_create_view,
    property_update_view,
    property_delete_view,
    lease_create_view,
    LeaseDetailView,
    lease_terminate_view,
    review_create_view,
    listing_create_view,
    payment_create_view,
    LeaseListView,
    lease_update_view,
#     ReviewDetailAPIView,
#     LeaseListCreateAPIView, 
#     LeaseDetailAPIView, 
#     LeaseTerminateAPIView,
#     # Additional views you might consider
#     lease_list_view,            # Assuming you want to list all leases
#     listing_list_view,          # Assuming you want to list all listings
)

from property_management.views import ReviewCreateView

urlpatterns = [
    # Property URLs
    path('properties/', property_list_view, name='property_list'),
    path('properties/<int:property_id>/', property_detail_view, name='property_detail'),
    path('properties/create/', property_create_view, name='property_create'),
    path('properties/<int:property_id>/update/', property_update_view, name='property_update'),
    path('properties/<int:property_id>/delete/', property_delete_view, name='property_delete'),
    path('properties/<int:property_id>/reviews/add/', review_create_view, name='review_create'),    
    # Lease URLs
    path('leases/', LeaseListView.as_view(), name='lease_list'),  # New view for listing all leases
    path('leases/create/<int:property_id>/', lease_create_view, name='lease_create'),
    path('leases/<int:lease_id>/', LeaseDetailView.as_view(), name='lease_detail'),
    path('leases/<int:lease_id>/terminate/', lease_terminate_view, name='lease_terminate'),
    path('leases/<int:lease_id>/update/', lease_update_view, name='lease_update'),
    



    # Listing URLs
    # path('listings/', listing_list_view, name='listing_list'),  # New view for listing all listings
    path('listings/create/', listing_create_view, name='listing_create'),
    
    # Payment URLs
    path('payments/create/<int:lease_id>/', payment_create_view, name='payment_create'),
]
