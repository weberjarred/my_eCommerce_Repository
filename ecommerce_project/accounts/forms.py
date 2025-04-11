from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    """
    RegistrationForm is a custom user registration form that extends the
    UserCreationForm. It includes additional fields for email and account type,
    and validates the uniqueness of the email address.

    Attributes:
        email (forms.EmailField): A required email field for the user.
        account_type (forms.ChoiceField): A required choice field to specify
            the type of account (Vendor or Buyer).

    Meta:
        model (User): The user model associated with this form.
        fields (list): The fields to include in the form, which are 'username',
            'email', 'password1', 'password2', and 'account_type'.

    Methods:
        clean_email(): Validates the email field to ensure that the provided
            email address is not already associated with an existing user in
            the database. Raises a ValidationError if the email is already
            in use.
    """
    email = forms.EmailField(required=True)
    account_type = forms.ChoiceField(
        choices=[("vendor", "Vendor"), ("buyer", "Buyer")], required=True
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "account_type",
        ]

    def clean_email(self):
        """
        Validates the email field to ensure that the provided email address
        is not already associated with an existing user in the database.

        Raises:
            forms.ValidationError: If the email address is already in use.

        Returns:
            str: The validated email address.
        """
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email address is already in use."
            )
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """
    CustomAuthenticationForm is a subclass of Django's built-in
    AuthenticationForm.

    This class can be extended to customize the login form by adding additional
    fields, validation logic, or overriding existing behaviour.

    Currently, it does not add any new functionality but serves as a
    placeholder for future customizations.

    Attributes:
        Inherits all attributes from AuthenticationForm.

    Methods:
        Inherits all methods from AuthenticationForm.
    """
    # Extend if you wish to customize the login form.
    pass
