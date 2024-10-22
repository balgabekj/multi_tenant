from django.urls import path
from .views import register, user_login, user_logout, tenant_dashboard, renter_dashboard

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('tenant_dashboard', tenant_dashboard, name='tenant_dashboard'), 
    path('renter_dashboard', renter_dashboard, name='renter_dashboard')
]

handler403 = 'django.views.defaults.permission_denied'

