from django.db import models
from store.models import Store


class Product(models.Model):
    store = models.ForeignKey(
        Store, on_delete=models.CASCADE, related_name="products"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(
        upload_to="product_images/", blank=True, null=True
    )

    # STOCK FIELD
    stock = models.PositiveIntegerField(
        default=0, help_text="Number of items in stock."
    )

    def __str__(self):
        return self.name