from django.contrib import admin
from django.urls import path, include
from .views import home
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
# Define schema view for Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="My API",
        default_version='v1',
        description="Description of my API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@myapi.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(AllowAny,),
)

router = routers.DefaultRouter()
urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('home/', home, name='home'),
    path('property_management/', include('property_management.urls')),
    path('blog_management/', include('blog_management.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
]
