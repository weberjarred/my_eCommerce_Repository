from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
    Configuration class for the 'store' application.

    This class inherits from Django's AppConfig and is used to configure
    application-specific settings for the 'store' app within the project.

    Attributes:
        default_auto_field (str): Specifies the default type of primary key
        field to use for models in the app. Defaults to
        "django.db.models.BigAutoField".
        name (str): The full Python path to the application,
        in this case "store".
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "store"
