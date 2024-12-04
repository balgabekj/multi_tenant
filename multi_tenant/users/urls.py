from django.urls import path
from .views import RenterLeasesView, UpdatePaymentMethodView, UserProfileView, prolongate_rental_agreement, register, renew_lease, terminate_lease, terminate_rental_agreement, user_login, user_logout, view_renting_property, tenant_dashboard, renter_dashboard, view_my_property

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('tenant_dashboard', tenant_dashboard, name='tenant_dashboard'),
    path('renter_dashboard', renter_dashboard, name='renter_dashboard'),

    # Tenant-specific actions
    path('rented-property/', view_renting_property, name='rented-property'),

    path('my-properties/', view_my_property, name='my-properties'),
]

handler403 = 'django.views.defaults.permission_denied'

