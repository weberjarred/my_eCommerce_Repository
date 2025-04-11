from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import (
    buyer_required,
)  # Import buyer_required if it exists in accounts.decorators
from products.models import Product
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# from django.urls import reverse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


@login_required
@buyer_required
def add_to_cart(request, product_id):
    """
    Handles adding a product to the shopping cart.

    Args:
        request (HttpRequest): The HTTP request object containing POST data
        and session information.
        product_id (int): The ID of the product to be added to the cart.

    Retrieves the product using the provided product_id and validates
    the quantity submitted via the form. Ensures the quantity is at least 1
    and does not exceed the available stock. Updates the cart stored in the
    product and quantity.

    If the quantity is invalid or exceeds stock, an error message is displayed,
    and the user is redirected to the product detail page.
    Success messages are displayed upon successful addition to the cart.

    Returns:
        HttpResponseRedirect: Redirects the user to the product detail page.
    """
    # Retrieve the product using the passed product_id
    product = get_object_or_404(Product, id=product_id)

    # Get the quantity from the form
    quantity_str = request.POST.get("quantity", "1")
    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1  # fallback if user entered invalid data

    # Logic to add product to the cart (stored in session or database)
    # Server-side logical check: quantity cannot exceed product.stock
    if quantity < 1:
        messages.error(request, "Quantity must be at least 1.")
        return redirect("products:product_detail", product_id=product_id)
    if quantity > product.stock:
        messages.error(request, "Not enough stock available.")
        return redirect("products:product_detail", product_id=product_id)

    # Using session-based cart
    cart = request.session.get("cart", {})
    # Add or update the quantity for this product
    cart[str(product_id)] = cart.get(str(product_id), 0) + quantity
    request.session["cart"] = cart

    messages.success(request, f"{product.name} × {quantity}, added to cart!")
    return redirect("products:product_detail", product_id=product_id)


@buyer_required
def view_cart(request):
    """
    Handles the display of the shopping cart for the current session.

    Retrieves the cart data from the session, calculates the total cost,
    and prepares a list of cart items with their details to be rendered
    in the cart template.

    Args:
        request (HttpRequest): The HTTP request object containing session data.

    Returns:
        HttpResponse: A rendered HTML page displaying the cart items
        and total cost.

    Session Variables:
        cart (dict): A dictionary where the keys are product IDs (int) and the
        values are quantities (int) of the products in the cart.

    Template:
        orders/cart.html: The template used to display the cart details.

    Raises:
        Http404: If a product in the cart does not exist in the database.
    """
    cart = request.session.get("cart", {})
    cart_items = []
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "item_total": item_total,
            }
        )
    return render(
        request, "orders/cart.html", {"cart_items": cart_items, "total": total}
    )


@buyer_required
@login_required(login_url="accounts:login")
def checkout(request):
    """
    Handles the checkout process for the user's cart.
    This function retrieves the cart from the session, creates an order,
    processes each item in the cart, updates product stock, calculates
    the total cost, and sends an invoice email to the user. If the cart
    is empty or a product is out of stock, appropriate messages are displayed.

    Args:
        request (HttpRequest): The HTTP request object containing user
        session and other request data.

    Returns:
        HttpResponse: Redirects the user to the product list page after
        successful checkout or to the cart view if an error occurs.

    Workflow:
        1. Retrieve the cart from the session.
        2. Check if the cart is empty; if so, display an error message
           and redirect.
        3. Create a new order for the logged-in user.
        4. Iterate through the cart items:
            - Retrieve the product and its price.
            - Create an OrderItem for each product.
            - Check stock availability.
            - Update stock if sufficient.
            - Handle out-of-stock scenarios with a warning message
              and redirect.
            - Calculate the total cost of the order.
        5. Save the total cost to the order.
        6. Clear the cart from the session.
        7. Generate and send an invoice email to the user.
        8. Display a success message and redirect to the product list page.

    Raises:
        Http404: If a product in the cart does not exist.
    """
    cart = request.session.get("cart", {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect("products:product_list")

    order = Order.objects.create(user=request.user)
    total = 0
    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        price = product.price
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=price
        )
        if product.stock >= quantity:
            product.stock -= quantity
            product.save()
        else:
            messages.warning(request, f"{product.name} is out of stock.")
            return redirect("orders:view_cart")
            # handle partial order or fail the checkout
        total += price * quantity

    order.total = total
    order.save()

    # Clear the cart after checkout.
    request.session["cart"] = {}
    # Generate and send invoice email.
    subject = f"Invoice for Order #{order.id}"
    message = render_to_string("orders/invoice_email.html", {"order": order})
    email = EmailMessage(
        subject, message, settings.EMAIL_HOST_USER, [request.user.email]
    )
    email.send()
    messages.success(
        request, "Checkout complete. An invoice has been sent to your email."
    )
    return redirect("products:product_list")


def remove_item(request, product_id):
    """
    Removes an item from the shopping cart stored in the session.

    Args:
        request (HttpRequest): The HTTP request object containing session data.
        product_id (int): The ID of the product to be removed from the cart.

    Behaviour:
        - Retrieves the current cart from the session.
        - Removes the specified product from the cart if it exists.
        - Updates the session with the modified cart.
        - Displays an informational message to the user indicating the item
          was removed.
        - Redirects the user to the cart display page.

    Returns:
        HttpResponseRedirect: A redirect to the cart display page.
    """
    cart = request.session.get("cart", {})
    product_key = str(product_id)

    # If the product is in the cart, remove it
    if product_key in cart:
        del cart[product_key]
        request.session["cart"] = cart

    # Provide a message or skip if you prefer
    messages.info(request, "Item removed from your cart.")

    # IMPORTANT: Redirect to your cart display page, NOT the checkout route
    # or wherever you show the updated cart
    return redirect("orders:view_cart")
