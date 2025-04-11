from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)
from rest_framework.response import Response
from rest_framework import status
from .serializers import StoreSerializer
from .models import Store
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated


@api_view(["GET"])
def list_stores(request):
    """
    Retrieve a list of all stores.

    This view fetches all store records from the database, serializes them
    using the StoreSerializer, and returns the serialized data as a response.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        Response: A Response object containing the serialized data
        of all stores.
    """
    stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def add_store(request):
    """
    Handles the creation of a new store.

    This view verifies that the vendor ID provided in the request data matches
    the ID of the currently logged-in user. If the IDs do not match, an error
    response is returned. If the data is valid, a new store is created and the
    serialized store data is returned.

    Args:
        request (HttpRequest): The HTTP request object containing user
        information and store data to be added.

    Returns:
        Response: A Response object containing:
            - Serialized store data with a 201 CREATED status if the store is
              successfully created.
            - An error message with a 400 BAD REQUEST status if the user ID
              does not match or if the provided data is invalid.
    """
    # Verify the vendor in the posted data matches the logged-in user
    if request.user.id != int(request.data.get("vendor", 0)):
        return Response(
            {"error": "User ID mismatch"}, status=status.HTTP_400_BAD_REQUEST
        )
    serializer = StoreSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def store_list(request):
    """
    Retrieve a list of stores. Optionally filter by vendor ID.

    Args:
        request (HttpRequest): The HTTP request object containing query
        parameters.

    Query Parameters:
        vendor (int, optional): The ID of the vendor to filter stores by.

    Returns:
        Response: A Response object containing serialized store data.
    """
    vendor_id = request.query_params.get("vendor", None)
    if vendor_id:
        stores = Store.objects.filter(vendor__id=vendor_id)
    else:
        stores = Store.objects.all()
    serializer = StoreSerializer(stores, many=True)
    return Response(serializer.data)
