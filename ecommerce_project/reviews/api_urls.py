from django.urls import path
from . import api_views

urlpatterns = [
    path(
        "list/<int:product_id>/",
        api_views.list_reviews,
        name="api_list_reviews",
    ),
]
