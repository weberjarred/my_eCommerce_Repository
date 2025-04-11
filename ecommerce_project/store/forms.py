from django import forms
from .models import Store


class StoreForm(forms.ModelForm):
    """
    StoreForm is a Django ModelForm for the Store model.

    This form allows users to create or update a Store instance by providing
    values for the following fields:
    - name: The name of the store.
    - description: A brief description of the store.
    - logo: An image file representing the store's logo.

    Attributes:
        Meta (class): Specifies the model and fields to include in the form.
    """
    class Meta:
        model = Store
        fields = ["name", "description", "logo"]
