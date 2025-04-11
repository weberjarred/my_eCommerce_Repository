from django.db import models
from django.contrib.auth.models import User


class Store(models.Model):
    """
    Represents a store in the eCommerce application.

    Attributes:
        vendor (User): A foreign key linking the store to its vendor (owner).
        name (str): The name of the store, with a maximum length of 255
        characters.
        description (str): A detailed description of the store.
        logo (ImageField): An optional image field for the store's logo,
        uploaded to the "store_logos/" directory.

    Methods:
        __str__(): Returns the name of the store as its string representation.
    """
    vendor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="stores"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    logo = models.ImageField(
        upload_to="store_logos/", blank=True, null=True
    )  # Optional store logo

    def __str__(self):
        return self.name
