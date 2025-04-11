from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from products.models import Product
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import buyer_required  # Import buyer_required


# Define the function to check if the user purchased the product
def check_if_user_purchased_product(user, product):
    """
    Check if a user has purchased a specific product.

    Args:
        user (User): The user whose purchase history is being checked.
        product (Product): The product to check for in the user's purchase
            history.

    Returns:
        bool: True if the user has purchased the product, False otherwise.

    Note:
        This function currently contains placeholder logic and always
        returns False.
        Replace the placeholder logic with the actual implementation to check
        the user's purchase history.
    """
    # Replace the following logic with the actual implementation
    # return product.orders.filter(user=user).exists()
    return False  # Temporarily return False until order logic is implemented.
    # Implement proper logic later.


@login_required
@buyer_required
@login_required(login_url="accounts:login")
def add_review(request, product_id):
    """
    Handle the addition or update of a product review by a user.
    This view allows a user to add a review for a specific product. If the user
    has already reviewed the product, the existing review is updated instead of
    creating a new one. Users are restricted to submitting only one review per
    product.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request and user data.
        product_id (int): The ID of the product being reviewed.

    Returns:
        HttpResponse: Renders the review form template for GET requests or
        redirects to the product detail page after successfully submitting the
        review for POST requests.

    Behavior:
        - If the user has already reviewed the product, the existing review is
          preloaded into the form for editing. This ensures that users can
          modify their existing review instead of creating a duplicate.
        - If the form is submitted and valid, the review is saved, and the user
          is redirected to the product detail page.
        - The review is marked as verified if the user has purchased the
          product.
        - Displays success messages upon successful submission.

    Template:
        reviews/add_review.html: The template used to render the review form.

    Raises:
        Http404: If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)

    # Check if the user has already reviewed the product.
    # I want to restrict users to only one review per product.
    existing_review = Review.objects.filter(
        product=product, reviewer=request.user
    ).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=existing_review)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.reviewer = request.user
            # Here you could add logic to mark review as verified
            # if the user purchased the product.
            review.verified = check_if_user_purchased_product(
                request.user, product
            )
            review.save()
            messages.success(request, "Your review has been submitted.")
            return redirect("products:product_detail", product_id=product.id)
    else:
        form = ReviewForm(instance=existing_review)

    return render(
        request, "reviews/add_review.html", {"form": form, "product": product}
    )


def review_list(request, product_id):
    """
    Handles the retrieval and display of reviews for a specific product.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The ID of the product for which reviews are to be
            retrieved.

    Returns:
        HttpResponse: A rendered HTML page displaying the list of reviews
        for the specified product.

    Raises:
        Http404: If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)
    reviews = product.reviews.all()
    return render(
        request,
        "reviews/review_list.html",
        {"reviews": reviews, "product": product}
    )
