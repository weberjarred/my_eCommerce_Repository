from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """
    Configuration class for the 'orders' application.

    This class defines the default settings for the 'orders' app, including
    the default type of primary key field for models and the app's name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "orders"
