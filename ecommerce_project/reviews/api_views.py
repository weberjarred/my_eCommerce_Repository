from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ReviewSerializer
from .models import Review


@api_view(["GET"])
def list_reviews(request, product_id):
    """
    Retrieve and return a list of reviews for a specific product.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product for which reviews
            are to be retrieved.

    Returns:
        Response: A Response object containing serialized review data
        for the specified product.
    """
    reviews = Review.objects.filter(product__id=product_id)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data)
