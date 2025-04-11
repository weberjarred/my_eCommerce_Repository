from django.urls import path
from . import api_views

urlpatterns = [
    path("list/", api_views.list_stores, name="api_list_stores"),
    path("add/", api_views.add_store, name="api_add_store"),
]
