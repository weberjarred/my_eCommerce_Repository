from django.urls import path
from django.shortcuts import render


def home(request):
    """
    Handles the request for the home page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered home page.
    """
    return render(request, "home.html")


urlpatterns = [
    path("", home, name="home"),
]
