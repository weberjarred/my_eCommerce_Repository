from django.http import HttpResponseForbidden
from functools import wraps


def vendor_required(view_func):
    """
    Decorator to restrict access to views for users with a specific account
    type. This decorator ensures that the user is authenticated and has a
    profile with an account type of "vendor". If the user does not meet these
    criteria, an HTTP 403 Forbidden response is returned.

    Args:
        view_func (function): The view function to be wrapped by the decorator.

    Returns:
        function: The wrapped view function that enforces the vendor access
        restriction.

    Raises:
        HttpResponseForbidden: If the user is not authenticated or does not
        have the required account type.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and if the user's profile
        # indicates a vendor.
        if (
            not request.user.is_authenticated
            or request.user.profile.account_type != "vendor"
        ):
            return HttpResponseForbidden(
                "You do not have permission to access this page."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view


def buyer_required(view_func):
    """
    Decorator to restrict access to a view to users with a "buyer" account
    type. This decorator checks if the user is authenticated and has a profile
    with an account type of "buyer". If the user does not meet these
    conditions, an HttpResponseForbidden is returned, preventing access
    to the view.

    Args:
        view_func (function): The view function to be wrapped by the decorator.

    Returns:
        function: The wrapped view function that enforces the "buyer" account
        type restriction.

    Raises:
        HttpResponseForbidden: If the user is not authenticated or does not
        have a "buyer" account type.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if (
            not request.user.is_authenticated
            or request.user.profile.account_type != "buyer"
        ):
            return HttpResponseForbidden(
                "Only buyers can perform this action."
            )
        return view_func(request, *args, **kwargs)

    return _wrapped_view
