from django.contrib import admin
from .models import Tenant, Renter
# Register your models here.
admin.site.register(Tenant)
admin.site.register(Renter)