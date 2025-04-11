from django.urls import path
from . import views

app_name = "orders"

urlpatterns = [
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.view_cart, name="view_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("remove/<int:product_id>/", views.remove_item, name="remove_item"),
]
