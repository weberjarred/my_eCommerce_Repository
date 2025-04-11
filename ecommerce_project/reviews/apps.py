from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """
    Configuration class for the 'reviews' application.

    This class inherits from Django's AppConfig and is used to define
    application-specific settings for the 'reviews' app.

    Attributes:
        default_auto_field (str): Specifies the default type of primary key
            field to use for models in this app. Defaults to
            "django.db.models.BigAutoField".
        name (str): The full Python path to the application,
            in this case "reviews".
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "reviews"
