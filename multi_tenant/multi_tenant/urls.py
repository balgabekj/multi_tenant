from django.contrib import admin
from django.urls import path, include
from .views import home
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('home', home, name='home'),
]
