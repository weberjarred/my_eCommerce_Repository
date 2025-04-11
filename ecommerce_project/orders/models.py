from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Order(models.Model):
    """
    Represents an order placed by a user in the eCommerce system.

    Attributes:
        user (ForeignKey): A reference to the user who placed the order.
            Deletes the order if the associated user is deleted.
        created_at (DateTimeField): The date and time when the order
            was created. Automatically set to the current date and time
            when the order is
            created.
        total (DecimalField): The total amount for the order, with a maximum
            of 10 digits and 2 decimal places. Defaults to 0.0.

    Methods:
        __str__(): Returns a string representation of the order in the format
            "Order #<id> by <username>".
    """
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"


class OrderItem(models.Model):
    """
    Represents an item in an order, linking a product to an order with a
    specified quantity and price.

    Attributes:
        order (ForeignKey): A reference to the associated Order.
        Deletes the item if the order is deleted.
        product (ForeignKey): A reference to the associated Product.
        Deletes the item if the product is deleted.
        quantity (PositiveIntegerField): The number of units of the product
        in the order. Defaults to 1.
        price (DecimalField): The price of the product at the time of the
            order, stored as a snapshot with up to 10 digits and 2 decimal
            places.

    Methods:
        __str__(): Returns a string representation of the order item in the
            format "quantity x product name".
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10, decimal_places=2
    )  # Price snapshot

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
