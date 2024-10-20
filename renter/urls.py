# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('leases/', views.lease_list, name='lease_list'),
    path('leases/create/', views.create_lease, name='create_lease'),
    path('lease/<int:lease_id>/', views.view_lease, name='view_lease'),
    path('lease/<int:lease_id>/manage/', views.manage_lease, name='manage_lease'),
    path('renter/<int:renter_id>/apartment/add/', views.add_apartment, name='add_apartment'),
    path('renter/<int:renter_id>/rent-due-alerts/', views.view_rent_due_alerts, name='view_rent_due_alerts'),
    path('renter/<int:renter_id>/announcement/', views.post_announcement, name='post_announcement'),
]
