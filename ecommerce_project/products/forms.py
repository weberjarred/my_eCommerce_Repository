from django import forms
from .models import Product


class ProductForm(forms.ModelForm):
    """
    ProductForm is a Django ModelForm for the Product model.

    This form is used to create or update Product instances. It includes
    the following fields:
    - name: The name of the product.
    - description: A detailed description of the product.
    - price: The price of the product.
    - image: An image representing the product.
    - stock: The quantity of the product available in stock.

    The form automatically maps these fields to the corresponding fields
    in the Product model.
    """
    class Meta:
        model = Product
        fields = [
            "name",
            "description",
            "price",
            "image",
            "stock"
        ]
