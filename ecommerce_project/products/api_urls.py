from django.urls import path
from . import api_views

urlpatterns = [
    path("list/", api_views.product_list, name="api_product_list"),
    path("add/", api_views.add_product, name="api_add_product"),
]
