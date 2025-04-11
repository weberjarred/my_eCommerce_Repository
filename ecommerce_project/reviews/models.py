from django.db import models
from django.contrib.auth.models import User
from products.models import Product
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    """
    Review model represents a product review submitted by a user.

    Attributes:
        RATING_CHOICES (list of tuple): A list of tuples representing rating
        choices (1 to 5). This ensures that the rating is within the valid
        range.
        product (ForeignKey): A foreign key to the Product model,
        representing the reviewed product.
        reviewer (ForeignKey): A foreign key to the User model,
        representing the user who submitted the review.
        rating (PositiveSmallIntegerField): The rating given by the reviewer,
        validated to be between 1 and 5.
        title (CharField): The title of the review, with a maximum length
        of 255 characters.
        content (TextField): The content of the review, which is optional
        and can be left blank.
        created_at (DateTimeField): The timestamp when the review was created,
        automatically set on creation.
        verified (BooleanField): Indicates whether the reviewer purchased
        the product (default is False).

    Methods:
        __str__(): Returns a string representation of the review, including
        the product name and reviewer username.
    """
    RATING_CHOICES = [(i, i) for i in range(1, 6)]  # 1 to 5

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(
        User, on_delete=models.CASCADE
    )  # reviewer is a user
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True)  # User comment
    created_at = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(
        default=False
    )  # True if the reviewer purchased the product

    def __str__(self):
        return f"Review for {self.product.name} by {self.reviewer.username}"
