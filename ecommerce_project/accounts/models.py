# accounts/models.py
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Profile model represents additional information associated with a user in
    the system.

    Attributes:
        user (OneToOneField): A one-to-one relationship with the User model,
        ensuring each user has a unique profile.
        ACCOUNT_TYPES (tuple): A tuple of account type choices, either "vendor"
        or "buyer".
        account_type (CharField): Specifies the type of account, with a maximum
        length of 50 characters. Defaults to "vendor".

    Methods:
        __str__(): Returns a string representation of the profile in the format
        "<username>'s profile".
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    ACCOUNT_TYPES = (
        ("vendor", "Vendor"),
        ("buyer", "Buyer"),
    )
    account_type = models.CharField(
        max_length=50, choices=ACCOUNT_TYPES, default="vendor"
    )

    def __str__(self):
        return f"{self.user.username}'s profile"
