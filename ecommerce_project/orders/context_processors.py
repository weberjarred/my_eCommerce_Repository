def cart_item_count(request):
    """
    Context processor to calculate the total number of items in the shopping
    cart.

    Args:
        request (HttpRequest): The HTTP request object containing session data.

    Returns:
        dict: A dictionary with the total number of items in the cart,
              accessible via the key 'cart_item_count'.
    """
    # If there's no cart in session, return 0
    cart = request.session.get("cart", {})
    # Sum all quantities
    total_items = sum(cart.values())
    return {"cart_item_count": total_items}
