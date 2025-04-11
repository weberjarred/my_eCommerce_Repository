from django.apps import AppConfig


class ProductsConfig(AppConfig):
    """
    Configuration class for the 'products' application.

    This class inherits from Django's AppConfig and is used to configure
    application-specific settings for the 'products' app within the project.

    Attributes:
        default_auto_field (str): Specifies the type of primary key to use for
            models in this app. Defaults to "django.db.models.BigAutoField".
        name (str): The full Python path to the application, in this case,
            "products".
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "products"
