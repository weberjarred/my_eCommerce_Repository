from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Store
from .models import Product


class ProductsTestCase(TestCase):
    """
    ProductsTestCase is a Django TestCase class designed to test the
    functionality of product-related views in the eCommerce application.
    It includes the following:

    Methods:
    - setUp: Prepares the test environment by creating a test client, a vendor
        user, a store associated with the vendor, and a product associated
        with the store.

    - test_product_list: Verifies that the product list view is accessible,
        returns a status code of 200, and contains the name of the test product
        in the response.

    - test_product_detail: Ensures that the product detail view is accessible,
      returns a status code of 200, and displays the correct product
      description in the response.
    """
    def setUp(self):
        """
        Set up the test environment for the product-related tests.

        This method initializes the following:
        - A test client instance for simulating HTTP requests.
        - A vendor user account with a username and password.
        - A store associated with the vendor, including its name
          and its description. This ensures that the store is properly
          associated with the vendor.
        - A product associated with the store, including its name, description,
          and price.
        """
        self.client = Client()
        self.vendor = User.objects.create_user(
            username="vendor", password="pass123"
        )
        self.store = Store.objects.create(
            vendor=self.vendor, name="Vendor Store", description="Store Desc"
        )
        self.product = Product.objects.create(
            store=self.store,
            name="Test Product",
            description="Desc",
            price=9.99
        )

    def test_product_list(self):
        """
        Test the product list view.

        This test ensures that the product list view is accessible via the
        "products:product_list" URL and that it returns a status code of 200.
        Additionally, it verifies that the response contains the name of the
        product being tested.
        """
        response = self.client.get(reverse("products:product_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.name)

    def test_product_detail(self):
        """
        Test the product detail view.

        This test ensures that the product detail page is accessible and
        displays the correct product information. It verifies that the HTTP
        response status code is 200 (OK) and that the product description
        is present in the response content.
        """
        response = self.client.get(
            reverse("products:product_detail", args=[self.product.id])
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.description)
