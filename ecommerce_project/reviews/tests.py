from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from store.models import Store
from .models import Review
from accounts.models import Profile


class ReviewsTestCase(TestCase):
    """
    ReviewsTestCase is a Django TestCase class that contains unit tests for the
    reviews functionality in the eCommerce application. It sets up the
    necessary test data, including users, profiles, a store, and a product,
    and provides test methods to verify the behavior of the review system.

    Methods:
        setUp():
            Prepares the test environment by creating a buyer user,
            a vendor user, their respective profiles, a store, and a product.
            This setup ensures that the test cases have the required data
            to execute.

        test_add_review():
            Tests the functionality of adding a review for a product.
            It verifies that a logged-in user can successfully submit a review
            by posting valid data to the "add_review" view.
            The test checks the response status code and ensures that the
            review is saved in the database.
    """
    def setUp(self):
        """
        Set up the test environment for the reviews app.

        This method initializes the following:
        - A test client for simulating HTTP requests.
        - A buyer user with the username "reviewer" and account type set to
          "buyer".
        - A vendor user with the username "vendor" and account type set to
          "vendor".
        - A store associated with the vendor user.
        - A product associated with the created store.

        Objects are created using `get_or_create` to ensure no duplicates
        are created.
        """
        self.client = Client()
        # Create a buyer user (reviewer)
        self.buyer = User.objects.create_user(
            username="reviewer", password="pass123"
        )
        # Instead of create(), use get_or_create()
        profile_buyer, created = Profile.objects.get_or_create(user=self.buyer)
        profile_buyer.account_type = "buyer"
        profile_buyer.save()

        # Create a vendor user
        self.vendor = User.objects.create_user(
            username="vendor", password="pass123"
        )
        profile_vendor, created = Profile.objects.get_or_create(
            user=self.vendor
        )
        profile_vendor.account_type = "vendor"
        profile_vendor.save()

        # Create a store and a product
        self.store = Store.objects.create(
            vendor=self.vendor, name="Vendor Store", description="Desc"
        )
        self.product = Product.objects.create(
            store=self.store,
            name="Test Product",
            description="Desc",
            price=10.00,
            stock=10,
        )

    def test_add_review(self):
        """
        Test the functionality of adding a review for a product.

        This test verifies that a logged-in user can successfully submit
        a review for a product by posting valid data to the "add_review"
        view. It checks the following:
        - The response status code is 302 (indicating a successful redirect).
        - A review with the specified title is created and exists in the
          database.

        Steps:
        1. Log in as a user with valid credentials.
        2. Submit a POST request with review data (title, content, and rating).
        3. Assert that the response status code is 302.
        4. Assert that the review is successfully saved in the database.
        """
        self.client.login(username="reviewer", password="pass123")
        data = {
            "title": "Great Product",
            "content": "I loved it!",
            "rating": 5,
        }
        response = self.client.post(
            reverse(
                "reviews:add_review",
                args=[self.product.id]
            ),
            data
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Review.objects.filter(title="Great Product").exists())
