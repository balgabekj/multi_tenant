from django.urls import path
from .views import RenterLeasesView, UpdatePaymentMethodView, UserProfileView, prolongate_rental_agreement, register, renew_lease, terminate_lease, terminate_rental_agreement, user_login, user_logout, view_renting_property, tenant_dashboard, renter_dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('tenant_dashboard', tenant_dashboard, name='tenant_dashboard'),
    path('renter_dashboard', renter_dashboard, name='renter_dashboard'),

    # Tenant-specific actions
    path('rented-property/', view_renting_property, name='rented-property'),
    path('terminate-agreement/', terminate_rental_agreement, name='terminate-agreement'),
    path('prolongate-agreement/', prolongate_rental_agreement, name='prolongate-agreement'),
    path('update-payment/', UpdatePaymentMethodView.as_view(), name='update-payment'),

    # Renter-specific actions
    path('leases/', RenterLeasesView.as_view(), name='renter-leases'),
    path('leases/renew/<int:lease_id>/', renew_lease, name='renew-lease'),
    path('leases/terminate/<int:lease_id>/', terminate_lease, name='terminate-lease'),
]

handler403 = 'django.views.defaults.permission_denied'

