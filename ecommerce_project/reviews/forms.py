from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    ReviewForm is a Django ModelForm for creating and updating
    Review instances.

    Attributes:
        Meta (class): Contains metadata for the form, including the associated
            model and the fields to include in the form.
            - model: Specifies the Review model as the associated model.
            - fields: A list of fields ["title", "content", "rating"]
              to include in the form. This ensures better readability
              and compliance with PEP 8.
            - widgets: A dictionary defining custom widgets for the form
              fields:
                - "title": A TextInput widget with a "form-control"
                  CSS class.
                - "content": A Textarea widget with a "form-control" CSS class,
                  3 rows,
                  and a placeholder text "Write your review here...".
                - "rating": A Select widget with choices from
                  Review.RATING_CHOICES and a "form-select" CSS class.
    """
    class Meta:
        model = Review
        fields = ["title", "content", "rating"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Write your review here...",
                }
            ),
            "rating": forms.Select(
                choices=Review.RATING_CHOICES, attrs={"class": "form-select"}
            ),
        }
