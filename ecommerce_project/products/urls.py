from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
    path(
        "create/<int:store_id>/",
        views.create_product,
        name="create_product",
    ),
    path("edit/<int:product_id>/", views.edit_product, name="edit_product"),
    path(
        "delete/<int:product_id>/",
        views.delete_product,
        name="delete_product",
    ),
    # e.g., /products/vendor/5/ will list products from vendor with id 5
    path(
        "vendor/<int:vendor_id>/",
        views.vendor_products,
        name="vendor_products",
    ),
]
