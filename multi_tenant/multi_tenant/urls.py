from django.contrib import admin
from django.urls import path, include
from .views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('home', home, name='home'),
    path('property_management/', include('property_management.urls')),
]
