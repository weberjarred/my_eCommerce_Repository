from django.urls import path
from . import views

app_name = "reviews"

urlpatterns = [
    path("add/<int:product_id>/", views.add_review, name="add_review"),
    path("list/<int:product_id>/", views.review_list, name="review_list"),
]
