from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from accounts.decorators import vendor_required  # Import vendor_required
# decorator
from .models import Product
from .forms import ProductForm
from store.models import Store
# from django.urls import reverse
from django.contrib import messages
from functions.tweet import Tweet  # For tweeting new products (Phase 2)
from django.contrib.auth.models import User


def product_list(request):
    """
    Handles the retrieval and display of a list of products.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A rendered HTML page displaying the list of products.
    """
    products = Product.objects.all()
    return render(
        request, "products/product_list.html", {"products": products}
    )


def product_detail(request, product_id):
    """
    View function to display the details of a specific product.

    Args:
        request (HttpRequest): The HTTP request object.
        product_id (int): The unique identifier of the product to retrieve.

    Returns:
        HttpResponse: The rendered HTML page displaying the product details.

    Raises:
        Http404: If the product with the given ID does not exist.
    """
    product = get_object_or_404(Product, id=product_id)
    return render(
        request, "products/product_detail.html", {"product": product}
    )


@login_required(login_url="accounts:login")
@vendor_required
def create_product(request, store_id):
    """
    Handles the creation of a new product for a specific store.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        store_id (int): The ID of the store where the product will be created.

    Returns:
        HttpResponse: Renders the product creation form or redirects to the
        vendor dashboard upon successful creation.

    Workflow:
        1. Retrieves the store object associated with the given store_id
           and the current user.
        2. If the request method is POST:
            - Validates the submitted ProductForm.
            - Saves the new product instance and associates it with the store.
            - Optionally attempts to tweet about the new product.
            - Displays a success message and redirects to the vendor dashboard.
        3. If the request method is not POST:
            - Displays an empty ProductForm for the user to fill out.

    Template:
        Renders the "products/product_form.html" template with the form
        and store context. This includes the form data and the store
        information for rendering the template.

    Exceptions:
        - If the tweet about the new product fails, logs the error and
          continues without interrupting the flow.
    """
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store
            product.save()
            # Phase 2: Optionally tweet about the new product.
            new_product_tweet = (
                f"New product available from {store.name}!\n"
                f"{product.name}\n"
                f"{product.description}"
            )
            tweet_data = {"text": new_product_tweet}
            try:
                Tweet().make_tweet(tweet_data)
            except Exception as e:
                print("Tweet failed:", e)
            messages.success(request, "Product created successfully.")
            return redirect("store:vendor_dashboard")
    else:
        form = ProductForm()
    return render(
        request,
        "products/product_form.html",
        {"form": form, "store": store}
    )


@login_required(login_url="accounts:login")
@vendor_required
def edit_product(request, product_id):
    """
    Handles the editing of a product by its vendor.
    This view allows a vendor to edit the details of a product they own.
    If the current user does not own the product, an access denied message
    is displayed, and the user is redirected to the vendor dashboard.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        product_id (int): The ID of the product to be edited.

    Returns:
        HttpResponse: Renders the product form template for GET requests or
        redirects to the vendor dashboard after successful form submission.

    Behaviour:
        - If the product does not exist, a 404 error is raised.
        - If the current user does not own the product, an error message is
          displayed, and the user is redirected.
        - For POST requests:
            - Validates and saves the submitted form data.
            - Displays a success message and redirects to the vendor dashboard.
        - For GET requests:
            - Displays the product form pre-filled with the product's current
              details.
    """
    product = get_object_or_404(Product, id=product_id)

    # Check if current user owns this product
    if product.store.vendor != request.user:
        # Show an Access Denied message and redirect
        messages.error(request, "Access Denied: You do not own this product.")
        return redirect("store:vendor_dashboard")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("store:vendor_dashboard")
    else:
        form = ProductForm(
            instance=product
        )
    return render(
        request,
        "products/product_form.html",
        {"form": form, "product": product}
    )


@login_required(login_url="accounts:login")
@vendor_required
def delete_product(request, product_id):
    """
    Handles the deletion of a product by its ID.
    This view ensures that only the vendor who owns the product can delete it.
    If the user does not own the product, an access denied message is
    displayed, and the user is redirected to the vendor dashboard.
    If the request method is POST, the product is deleted, and a success
    message is displayed. Otherwise, a confirmation page is rendered.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        product_id (int): The ID of the product to be deleted.

    Returns:
        HttpResponse: A redirect to the vendor dashboard upon successful
            deletion or access denial, or a rendered confirmation page
            for GET requests.
    """
    product = get_object_or_404(Product, id=product_id)

    # Check if current user owns this product
    if product.store.vendor != request.user:
        # Show an Access Denied message and redirect
        messages.error(request, "Access Denied: You do not own this product.")
        return redirect("store:vendor_dashboard")

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("store:vendor_dashboard")
    return render(
        request,
        "products/product_delete_confirm.html",
        {"product": product}
    )


@login_required
def vendor_products(request, vendor_id):
    """
    Handles the display of all products associated with a specific vendor.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        vendor_id (int): The unique identifier of the vendor whose products
            are to be displayed.

    Returns:
        HttpResponse: A rendered HTML page displaying the vendor's products.

    Raises:
        Http404: If the vendor with the given ID does not exist.

    Template:
        products/vendor_products.html

    Context:
        vendor (User): The vendor object corresponding to the given vendor_id.
        products (QuerySet): A queryset of Product objects associated with
            the vendor's store.
    """
    vendor = get_object_or_404(User, id=vendor_id)
    products = Product.objects.filter(store__vendor=vendor)
    context = {
        "vendor": vendor,
        "products": products,
    }
    return render(request, "products/vendor_products.html", context)
