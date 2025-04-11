from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """
    Django application configuration for the 'accounts' app.
    This class is responsible for configuring the 'accounts' application,
    including specifying its name and performing any application-specific
    initialization when the application is ready.

    Attributes:
        default_auto_field (str): Specifies the type of primary key to use for
            models in this application. Defaults to
            "django.db.models.BigAutoField".
        name (str): The name of the application, used for application
            registration.

    Methods:
        ready():
            Overrides the default ready method to perform initialization tasks
            specific to the 'accounts' app. This includes importing the
            `accounts.signals` module to ensure that signal handlers are
            registered when the application starts.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        """
        Overrides the ready method to perform application-specific
        initialization.

        This method is called when the application is ready to be used.
        It imports the `accounts.signals` module to ensure that signal handlers
        are registered when the application starts. The `# noqa: F401` comment
        suppresses linting warnings for the unused import, as the import is
        necessary for its side effects.
        """
        # Importing accounts.signals to register signal handlers
        import accounts.signals  # noqa: F401
