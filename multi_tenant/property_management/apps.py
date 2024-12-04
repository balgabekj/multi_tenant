from django.apps import AppConfig


class PropertyManagementConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "property_management"
    def ready(self):
        import property_management.signals  # Import the signals

