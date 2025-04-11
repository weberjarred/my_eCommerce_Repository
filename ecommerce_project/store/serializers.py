from rest_framework import serializers
from .models import Store


class StoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Store model.

    This serializer is used to convert Store model instances into JSON format
    and vice versa. It includes the following fields:
    - id: The unique identifier of the store.
    - vendor: The vendor associated with the store.
    - name: The name of the store.
    - description: A brief description of the store.
    - logo: The logo image of the store.

    The serializer is based on Django's ModelSerializer, which automatically
    generates fields based on the specified model.
    """
    class Meta:
        model = Store
        fields = [
            "id",
            "vendor",
            "name",
            "description",
            "logo"
        ]
