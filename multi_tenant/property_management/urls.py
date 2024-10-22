from django.urls import path
from .views import (
    property_list_view,
    property_detail_view,
    property_create_view,
    property_update_view,
    property_delete_view,
    lease_create_view,
    lease_detail_view,
    lease_terminate_view,
    review_create_view,
    listing_create_view,
    payment_create_view,
)

urlpatterns = [
    path('properties/', property_list_view, name='property_list'),
    path('properties/<int:property_id>/', property_detail_view, name='property_detail'),
    path('properties/create/', property_create_view, name='property_create'),
    path('properties/<int:property_id>/update/', property_update_view, name='property_update'),
    path('properties/<int:property_id>/delete/', property_delete_view, name='property_delete'),
    path('leases/create/<int:property_id>/', lease_create_view, name='lease_create'),
    path('leases/<int:lease_id>/', lease_detail_view, name='lease_detail'),
    path('leases/<int:lease_id>/terminate/', lease_terminate_view, name='lease_terminate'),
    path('properties/<int:property_id>/reviews/create/', review_create_view, name='review_create'),
    path('listings/create/<int:property_id>/', listing_create_view, name='listing_create'),
    path('payments/create/<int:lease_id>/', payment_create_view, name='payment_create'),
]
