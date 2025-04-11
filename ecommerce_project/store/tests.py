from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Store


class StoreTestCase(TestCase):
    """StoreTestCase is a test suite for the store application.
    This test case class contains unit tests to verify the functionality of
    the store-related views, including creating, editing, and deleting a store.
    It uses Django's TestCase framework to set up a test environment and
    simulate HTTP requests.

    Methods:
        setUp():
            Prepares the test environment by initializing the test client,
            creating a test user, logging in the user, and setting up a test
            store associated with the user.

        test_create_store():
            Tests the creation of a new store using the "create_store" view.
            Verifies that the store is successfully created and exists in the
            database.

        test_edit_store():
            Tests the functionality of editing a store using the "edit_store"
            view. Verifies that the store's details are updated correctly in
            the database.

        test_delete_store():
            Tests the deletion of a store using the "delete_store" view.
            Verifies that the store is successfully removed from the database.
    """
    def setUp(self):
        """
        Set up the test environment for the store application.

        This method initializes the test client, creates a test user,
        logs in the user, and sets up a test store associated with the user.

        Attributes:
            client (Client): The Django test client used to simulate HTTP
                requests.
            user (User): The test user created for authentication and
                association with the store.
            store (Store): The test store instance created for testing
                purposes.
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username="vendor1", password="pass123"
        )
        self.client.login(username="vendor1", password="pass123")
        self.store = Store.objects.create(
            vendor=self.user, name="Test Store", description="Test description"
        )

    def test_create_store(self):
        """
        Test the creation of a new store.

        This test verifies that a store can be successfully created using the
        "create_store" view. It checks that the response status code is 302
        (indicating a successful redirect) and ensures that the store with the
        specified name exists in the database after the request.

        Steps:
        1. Define the data for the new store, including its name
           and description. This ensures that the data is properly
           formatted for the test.
        2. Send a POST request to the "create_store" view with the provided
           data.
        3. Assert that the response status code is 302.
        4. Assert that a store with the specified name exists in the database.
        """
        data = {"name": "New Store", "description": "New description"}
        response = self.client.post(reverse("store:create_store"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Store.objects.filter(name="New Store").exists())

    def test_edit_store(self):
        """
        Test the functionality of editing a store.

        This test verifies that a store's details can be successfully updated
        via a POST request to the "edit_store" view. It checks that:
        - The response status code is 302 (indicating a successful redirect).
        - The store's details in the database are updated correctly.
        """
        data = {"name": "Updated Store", "description": "Updated description"}
        response = self.client.post(
            reverse("store:edit_store", args=[self.store.id]), data
        )
        self.assertEqual(response.status_code, 302)
        self.store.refresh_from_db()
        self.assertEqual(self.store.name, "Updated Store")

    def test_delete_store(self):
        """
        Test case for deleting a store.

        This test ensures that a store can be successfully deleted via a POST
        request to the "delete_store" view. It verifies the following:
        - The response status code is 302 (indicating a redirect).
        - The store is no longer present in the database after the deletion.
        """
        response = self.client.post(
            reverse("store:delete_store", args=[self.store.id])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Store.objects.filter(id=self.store.id).exists())
