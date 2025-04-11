from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProductSerializer
from .models import Product
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def product_list(request):
    """
    Handles the retrieval of a list of products, optionally filtered by
    store ID, or by vendor ID.

    Args:
        request (HttpRequest): The HTTP request object containing query
        parameters.

    Query Parameters:
        store (str, optional): The ID of the store to filter products by.
        If not provided, all products are returned.

    Returns:
        Response: A Response object containing serialized product data
        in JSON format.
    """
    store_id = request.query_params.get("store", None)
    if store_id:
        products = Product.objects.filter(store__id=store_id)
    else:
        products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_product(request):
    """
    Handles the creation of a new product.

    This view function accepts a POST request containing product data,
    validates the data using the ProductSerializer, and saves the product
    to the database if the data is valid. If the data is invalid, it returns
    an error response.

    Args:
        request (HttpRequest): The HTTP request object containing the product
        data in the request body.

    Returns:
        Response: A Response object containing the serialized product data
        and a status code of 201 (Created) if the product is successfully
        created. If the data is invalid, returns a Response object with the
        validation errors and a status code of 400 (Bad Request).
    """
    serializer = ProductSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
