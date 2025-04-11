from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AccountsTestCase(TestCase):
    """
    AccountsTestCase is a test case class for testing the functionality of the
    accounts application in a Django project. It includes tests for user
    registration, login, and logout functionalities.

    Methods:
        setUp():
            Sets up the test environment by initializing the test client and
            creating a test user with predefined credentials for authentication
            tests.

        test_registration():
            Tests the user registration functionality by verifying that a new
            user can successfully register with valid data. Ensures the
            response status code is 302 (redirect) and that the user is
            created in the database.

        test_login():
            Tests the login functionality by verifying that a user can log in
            with valid credentials. Ensures the response status code is 302
            (redirect) after a successful login.

        test_logout():
            Tests the logout functionality by verifying that a logged-in user
            can successfully log out. Ensures the response status code is 302
            (redirect) after logout.
    """
    def setUp(self):
        """
        Set up the test environment for the test cases.

        This method is called before each test case is executed. It initializes
        the test client and creates a test user with predefined credentials
        (username, password, and email) to be used in login-related tests.

        Attributes:
            client (Client): The Django test client used to simulate requests.
            user (User): The test user created for authentication tests.
        """
        # Arrange: create a test user for login tests.
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com",
        )

    def test_registration(self):
        """
        Test the user registration functionality.

        This test verifies that a new user can successfully register by
        submitting valid data to the registration endpoint. It checks that
        the response status code indicates a redirect (302). It also
        confirms that the new user is created in the database.

        Test Steps:
        1. Arrange: Prepare valid registration data, including username, email,
           account type, and matching passwords.
        2. Act: Submit a POST request to the registration endpoint
           with the data. Ensure the data includes valid and matching
           passwords.
        3. Assert: Verify that the response status code is 302 (redirect)
           and that the user with the specified username exists in the
           database.
        """
        # Arrange
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "account_type": "buyer",
            "password1": "newpass123",
            "password2": "newpass123",
        }
        # Act
        response = self.client.post(reverse("accounts:register"), data)
        # Assert: registration redirects and user exists.
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_login(self):
        """
        Test the login functionality of the accounts app.

        This test verifies that a POST request to the login view with valid
        credentials successfully logs in the user and redirects to the
        appropriate page.

        Steps:
        1. Prepare valid login credentials (username and password).
        2. Send a POST request to the login view with the credentials.
        3. Assert that the response status code is 302, indicating a successful
           redirection after login.
        """
        # Act
        data = {"username": "testuser", "password": "testpass123"}
        response = self.client.post(reverse("accounts:login"), data)
        # Assert: successful login should redirect.
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        """
        Tests the logout functionality of the application.

        This test ensures that a logged-in user is successfully logged out
        and redirected to the appropriate page.

        Steps:
        1. Log in a test user using the client.
        2. Perform a GET request to the logout view.
        3. Verify that the response status code is 302 (redirection).

        Expected Outcome:
        - The user is logged out, and the response indicates a redirection.
        """
        # Arrange: log in first.
        self.client.login(username="testuser", password="testpass123")
        # Act
        response = self.client.get(reverse("accounts:logout"))
        # Assert: logout redirects.
        self.assertEqual(response.status_code, 302)
