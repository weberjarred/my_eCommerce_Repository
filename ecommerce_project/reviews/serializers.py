from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model.

    This serializer is used to convert Review model instances into JSON format
    and vice versa. It includes the following fields:
    - id: The unique identifier for the review.
    - product: The product being reviewed.
    - reviewer: The user who wrote the review.
    - title: The title of the review.
    - content: The main content of the review.
    - rating: The rating given to the product.
    - verified: A boolean indicating if the review is verified.
    - created_at: The timestamp when the review was created.
    """
    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "reviewer",
            "title",
            "content",
            "rating",
            "verified",
            "created_at",
        ]
