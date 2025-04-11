from django.shortcuts import render, redirect, get_object_or_404
from accounts.decorators import vendor_required  # Import vendor_required
from django.contrib.auth.decorators import login_required
from .models import Store
from products.models import Product
from .forms import StoreForm
# from django.urls import reverse
from django.contrib import messages
from functions.tweet import Tweet  # For Phase 2 Twitter integration


@login_required(login_url="accounts:login")
@vendor_required
def vendor_dashboard(request):
    # Display stores belonging to the logged-in vendor.
    stores = Store.objects.filter(vendor=request.user)
    return render(request, "store/vendor_dashboard.html", {"stores": stores})


@login_required(login_url="accounts:login")
@vendor_required
def create_store(request):
    """
    Handle the creation of a new store by a vendor.
    This view processes a POST request containing store details submitted via a
    form. If the form is valid, it saves the store instance, associates it
    with the logged-in user (vendor), and optionally sends a tweet announcing
    the new store. If the request method is not POST, it renders an empty
    form for creating a store.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.

    Returns:
        HttpResponse: Redirects to the vendor dashboard upon successful
        store creation. Otherwise, renders the store creation form template.

    Raises:
        Exception: Logs any errors that occur while attempting to send a tweet,
        but does not interrupt the flow of the application.

    Template:
        store/store_form.html: The template used to render the store creation
        form.

    Messages:
        Success: Displays a success message when the store is created
        successfully.

    Notes:
        - The `StoreForm` is used to validate and save the store data.
        - The `Tweet` class is used to send a tweet about the new store.
        - The logged-in user is assumed to be the vendor creating the store.
    """
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES)
        if form.is_valid():
            store = form.save(commit=False)
            # Assuming vendor is the logged-in user
            store.vendor = request.user
            store.save()
            form.save_m2m()  # If there are many-to-many fields

            # Phase 2: Send a tweet about the new store.
            new_store_tweet = (
                f"New store open on eCommerce!\n"
                f"{store.name}\n\n"
                f"{store.description}"
            )
            tweet_data = {"text": new_store_tweet}
            try:
                # Ensure that the Tweet instance is created.
                if not hasattr(Tweet, "_instance") or Tweet._instance is None:
                    tweet_obj = (
                        Tweet()
                    )  # This should create and set the singleton instance.
                else:
                    tweet_obj = Tweet._instance
                tweet_data = {
                    "text": (
                        f"New store open on eStore!\n{store.name}\n"
                        f"{store.description}"
                    )
                }
                tweet_obj.make_tweet(tweet_data)
            except Exception as e:
                # Log the error but do not interrupt the flow.
                print("Error sending tweet:", e)

            messages.success(request, "Store created successfully.")

            return redirect("store:vendor_dashboard")
    else:
        form = StoreForm()
    return render(request, "store/store_form.html", {"form": form})
    # store_form.html is a template file
    # that contains the form for creating a store


@login_required(login_url="accounts:login")
@vendor_required
def edit_store(request, store_id):
    """
    Handles the editing of a store by a vendor.

    This view retrieves a store instance based on the provided store ID and
    ensures that the requesting user is the vendor associated with the store.
    If the request method is POST, it processes the submitted form data to
    update the store. If the form is valid, the store is updated, and the user
    is redirected to the vendor dashboard with a success message. If the
    request method is not POST, it displays a form pre-filled with the store's
    current data.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.
        store_id (int): The ID of the store to be edited.

    Returns:
        HttpResponse: Renders the store form template with the form context
        if the request method is GET or the form is invalid. Redirects to the
        vendor dashboard if the form is successfully submitted and valid.

    Raises:
        Http404: If the store with the given ID does not exist or the
        requesting user is not the vendor associated with the store.
    """
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        form = StoreForm(request.POST, request.FILES, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Store updated successfully.")
            return redirect("store:vendor_dashboard")
    else:
        form = StoreForm(instance=store)
    return render(request, "store/store_form.html", {"form": form})


@login_required(login_url="accounts:login")
@vendor_required
def delete_store(request, store_id):
    """
    Handle the deletion of a store by a vendor.

    This view allows a vendor to delete their store. If the request method is
    POST, the store is deleted, and the user is redirected to the vendor
    dashboard with a success message. If the request method is not POST, a
    confirmation
    is rendered.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.
        store_id (int): The ID of the store to be deleted.

    Returns:
        HttpResponse: A rendered confirmation page if the request method is not
        POST.
        HttpResponseRedirect: A redirect to the vendor dashboard if the store
        is successfully deleted.

    Raises:
        Http404: If the store with the given ID does not exist or does not
        belong to the current user.
    """
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    if request.method == "POST":
        store.delete()
        messages.success(request, "Store deleted successfully.")
        return redirect("store:vendor_dashboard")
    return render(request, "store/store_delete_confirm.html", {"store": store})


@login_required
@vendor_required
def store_products(request, store_id):
    """
    Handles the display of products for a specific store owned by the
    logged-in vendor.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.
        store_id (int): The ID of the store whose products are to be displayed.

    Returns:
        HttpResponse: Renders the "store/store_products.html" template
        with the store and its products.

    Raises:
        Http404: If the store does not exist or does not belong to the
        logged-in vendor.
    """
    # Ensure the store belongs to the logged-in vendor
    store = get_object_or_404(Store, id=store_id, vendor=request.user)
    products = Product.objects.filter(store=store)
    return render(
        request,
        "store/store_products.html",
        {"store": store, "products": products}
    )
