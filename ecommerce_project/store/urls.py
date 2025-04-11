from django.urls import path
from . import views

app_name = "store"

urlpatterns = [
    path("dashboard/", views.vendor_dashboard, name="vendor_dashboard"),
    path("create/", views.create_store, name="create_store"),
    path("edit/<int:store_id>/", views.edit_store, name="edit_store"),
    path("delete/<int:store_id>/", views.delete_store, name="delete_store"),
    # New route for listing store products
    path(
        "<int:store_id>/products/",
        views.store_products,
        name="store_products",
    ),
]
