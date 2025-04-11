from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
# from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator

from .forms import RegistrationForm, CustomAuthenticationForm
from .models import Profile  # Import the Profile model


def register(request):
    """
    Handles user registration, profile creation, and account type assignment.
    This view processes a user registration form.

    If the form is valid, it:
    1. Saves the user object.
    2. Creates or retrieves a Profile object associated with the user.
    3. Updates the Profile's account_type field based on the form's input.
    4. Logs the user in.
    5. Redirects the user to the appropriate dashboard or product list
       based on their account type.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.

    Returns:
        HttpResponse: Renders the registration form for GET requests or
        redirects to the appropriate page after successful registration.
    """
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            # 1) Save the User object
            user = form.save()

            # 2) Create or get the Profile for the new user
            profile, created = Profile.objects.get_or_create(user=user)

            # 3) Retrieve the chosen account_type from the form
            account_type = form.cleaned_data.get("account_type")

            # Brute force update the Profile's account_type directly:
            # Profile.objects.filter(user=user).update(account_type=account_type)

            """
            This tells Django to only update the specified field, ensuring
            that the form’s choice overrides the default even if the Profile
            was already created with the default value.
            """
            user.profile.account_type = account_type
            # Force update this field
            user.profile.save(update_fields=["account_type"])

            # 4) Assign it to the Profile
            # profile.account_type = account_type
            # profile.save()

            # Optionally, reload the profile instance if you need to use it
            # immediately.
            # profile.refresh_from_db()

            # 5) Log the user in and redirect
            login(request, user)
            if account_type == "vendor":
                return redirect("store:vendor_dashboard")
            else:
                return redirect("products:product_list")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


def user_login(request):
    """
    Handle user login functionality.

    This view processes both GET and POST requests for user authentication.
    On a POST request, it validates the submitted login form and logs in the
    user if the credentials are correct. Depending on the user's account type,
    it redirects them to the appropriate dashboard or product list page.
    On a GET request, it renders the login form.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.

    Returns:
        HttpResponse: A rendered login page for GET requests or a redirect
        to the appropriate page for successful logins.
    """
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully.")
            # Redirect based on the user's account type
            if (
                hasattr(user, "profile")
                and user.profile.account_type == "vendor"
            ):
                return redirect("store:vendor_dashboard")
            else:
                return redirect("products:product_list")
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def user_logout(request):
    """
    Logs out the currently authenticated user and redirects them
    to the login page.

    This view function handles the user logout process by calling Django's
    `logout` function to terminate the user's session. It also displays an
    informational
    message indicating that the user has logged out successfully.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.

    Returns:
        HttpResponseRedirect: A redirect response to the login page.
    """
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect("accounts:login")


def password_reset_request(request):
    """
    Handles password reset requests by sending a password reset email
    to the user.

    This view processes POST requests containing an email address, checks if
    there are any users associated with the provided email, and sends a
    password reset email to each associated user. If no users are found,
    an error message is displayed. For GET requests, it renders the password
    reset form.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
        about the request.

    Returns:
        HttpResponse: Renders the password reset form for GET requests or
        redirects to the login page with a success message for valid POST
        requests.

        Displays an error message if no user is associated with the provided
        email.
    """
    if request.method == "POST":
        email = request.POST.get("email")
        associated_users = User.objects.filter(email=email)
        if associated_users.exists():
            for user in associated_users:
                subject = "Password Reset Requested"
                email_template_name = "accounts/password_reset_email.txt"
                context = {
                    "email": user.email,
                    "domain": request.META["HTTP_HOST"],
                    "site_name": "eCommerce Site",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email_body = render_to_string(email_template_name, context)
                email_message = EmailMessage(
                    subject, email_body, to=[user.email]
                )
                email_message.send()
            messages.success(
                request, "A password reset link has been sent to your email."
            )
            return redirect("accounts:login")
        else:
            messages.error(
                request, "No user is associated with this email address."
            )
    return render(request, "accounts/password_reset.html")


def password_reset_confirm(request, uidb64=None, token=None):
    """
    Handles the password reset confirmation process.

    This view verifies the validity of the password reset link, checks the
    provided token, and allows the user to reset their password if the link
    is valid. If the link is invalid or expired, an error message is displayed.

    Args:
        request (HttpRequest): The HTTP request object containing metadata
            about the request.
        uidb64 (str, optional): Base64 encoded user ID. Defaults to None.
        token (str, optional): Token used to verify the password reset link.
            Defaults to None.

    Returns:
        HttpResponse: Renders the password reset page with appropriate context
        or redirects to the login page upon successful password reset.

    Behaviour:
        - Decodes the user ID from the provided `uidb64` and retrieves the
          corresponding user.
        - Validates the token using Django's default token generator.
        - If the link is valid and the request method is POST:
            - Checks if the new password and confirmation password match.
            - Updates the user's password and redirects to the login page
              with a success message.
        - If the link is invalid or expired:
            - Displays an error message and renders the reset password page
              with an invalid link context.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == "POST":
            new_password = request.POST.get("password")
            confirm_password = request.POST.get("password_confirm")
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(
                    request, "Password has been reset. You can now log in."
                )
                return redirect("accounts:login")
            else:
                messages.error(request, "Passwords do not match.")
        return render(
            request, "accounts/reset_password.html", {"validlink": True}
        )
    else:
        messages.error(
            request,
            "The reset password link is invalid or has expired."
        )
        return render(
            request, "accounts/reset_password.html", {"validlink": False}
        )
