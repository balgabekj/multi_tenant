from django.urls import path
from .views import (
    RenterLeasesView, UserProfileView, register, renter_dashboard, 
    terminate_rental_agreement, user_login, user_logout, view_my_property, 
    view_renting_property, tenant_dashboard, renew_lease, terminate_lease, home
)
from users.views import ProlongateRentalAgreementView, UpdatePaymentMethodAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', home, name='home'),

    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('tenant_dashboard', tenant_dashboard, name='tenant_dashboard'),
    path('renter_dashboard', renter_dashboard, name='renter_dashboard'),

    # Tenant-specific actions
    path('rented-property/', view_renting_property, name='rented-property'),
    path('api/terminate-agreement/', terminate_rental_agreement, name='terminate-agreement'),
    path('api/prolongate-agreement/', ProlongateRentalAgreementView.as_view(), name='prolongate-agreement'),
    path('api/update-payment/', UpdatePaymentMethodAPIView.as_view(), name='update-payment'),

    # Renter-specific actions
    path('my-properties/', view_my_property, name='my-properties'),
    path('renter-leases/', RenterLeasesView.as_view(), name='renter-leases'),
    path('renew-lease/<int:lease_id>/', renew_lease, name='renew-lease'),
    path('terminate-lease/<int:lease_id>/', terminate_lease, name='terminate-lease'),
]

handler403 = 'django.views.defaults.permission_denied'
