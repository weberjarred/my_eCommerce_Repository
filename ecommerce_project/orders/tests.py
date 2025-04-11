from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from products.models import Product
from store.models import Store
from .models import Order
from accounts.models import Profile


class OrdersTestCase(TestCase):
    """
    OrdersTestCase is a test case class for testing the functionality of the
    orders app in a Django project.
    This class includes:
    - A setup method to initialize the test environment, including creating
      test users, a store, and a product.
    - A test method to verify the process of adding a product to the cart
      and completing the checkout.

    Methods:
        setUp():
            Sets up the test environment by creating:
            - A buyer user with a "buyer" account type.
            - A vendor user with a "vendor" account type.
        test_add_to_cart_and_checkout():
            Tests the following:
            - Adding a product to the cart by simulating session data.
            - Logging in as a buyer user.
            - Accessing the checkout view and verifying a successful redirect.
            - Confirming that an order is created for the buyer user.
            - Ensuring the cart is cleared from the session after checkout.
        client (Client): The test client for simulating HTTP requests.
        buyer (User): The buyer user instance.
        vendor (User): The vendor user instance.
        store (Store): The store instance associated with the vendor.
        product (Product): The product instance associated with the store.
    """
    def setUp(self):
        """
        Set up the test environment for the orders app.

        This method initializes the following:
        - A test client for simulating HTTP requests.
        - A buyer user with a profile set to the "buyer" account type.
        - A vendor user with a profile set to the "vendor" account type.
        - A store associated with the vendor user.
        - A product associated with the store.

        Attributes:
            self.client (Client): The test client for HTTP requests.
            self.buyer (User): The buyer user instance.
            self.vendor (User): The vendor user instance.
            self.store (Store): The store instance associated with the vendor.
            self.product (Product): The product instance associated with the
            store.
        """
        self.client = Client()
        # Create a buyer user
        self.buyer = User.objects.create_user(
            username="buyer", password="pass123", email="buyer@example.com"
        )
        profile_buyer, created = Profile.objects.get_or_create(user=self.buyer)
        profile_buyer.account_type = "buyer"
        profile_buyer.save()

        # Create a vendor user for the store
        self.vendor = User.objects.create_user(
            username="vendor", password="pass123"
        )
        profile_vendor, created = Profile.objects.get_or_create(
            user=self.vendor
        )
        profile_vendor.account_type = "vendor"
        profile_vendor.save()

        # Create a store with the vendor and a product in that store
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

    def test_add_to_cart_and_checkout(self):
        """
        Test the process of adding a product to the cart and completing the
        checkout.

        Steps:
        1. Simulate adding a product to the cart by updating the session data.
        2. Log in as a buyer user.
        3. Access the checkout view and verify that it redirects successfully
           (status code 302).
        4. Confirm that an order is created for the logged-in buyer.
        5. Verify that the cart in the session is cleared after checkout.

        Assertions:
        - The response status code of the checkout view is 302 (redirect).
        - An order is created and associated with the buyer user.
        - The cart in the session is empty after checkout.
        """
        # Simulate adding a product to the cart
        session = self.client.session
        session["cart"] = {str(self.product.id): 2}
        session.save()
        # Login as buyer
        self.client.login(username="buyer", password="pass123")
        response = self.client.get(reverse("orders:checkout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.filter(user=self.buyer).count(), 1)
        session = self.client.session
        self.assertEqual(session.get("cart"), {})
