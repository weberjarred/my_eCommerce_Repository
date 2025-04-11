from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer for the Product model.

    This serializer is used to convert Product model instances into JSON format
    and vice versa. It includes the following fields:
    - id: The unique identifier for the product.
    - store: The store associated with the product.
    - name: The name of the product.
    - description: A detailed description of the product.
    - price: The price of the product.
    - stock: The available stock quantity of the product.
    - image: The image associated with the product.

    The serializer is based on Django's ModelSerializer, which automatically
    generates fields based on the specified model.
    """
    class Meta:
        model = Product
        fields = [
            "id",
            "store",
            "name",
            "description",
            "price",
            "stock",
            "image"
        ]
