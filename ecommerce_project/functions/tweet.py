import json
from requests_oauthlib import OAuth1Session
import datetime


class Tweet:
    """
    The `Tweet` class provides functionality to interact with the Twitter API
    using OAuth 1.0a authentication. It implements the Singleton design pattern
    to ensure only one instance of the class is created. The class allows users
    to authenticate with the Twitter API and post tweets.

        CONSUMER_KEY (str): The consumer key for the Twitter application.
        CONSUMER_SECRET (str): The consumer secret for the Twitter application.
        _instance (Tweet): The singleton instance of the `Tweet` class.

    Methods:
        __new__(cls):
            Ensures only one instance of the `Tweet` class is created. If an
            instance already exists, it returns the existing instance.
            Otherwise, it creates a new instance and initializes
            authentication.

        authenticate():
            Authenticates the user with the Twitter API using OAuth 1.0a. This
            involves fetching a request token, directing the user to authorize
            the application, exchanging the PIN for an access token, and
            creating an authenticated session for making API requests.

        make_tweet(tweet):
            Posts a tweet to Twitter using the authenticated session. The tweet
            content is dynamically appended with a timestamp to ensure
            uniqueness.
    """
    # Replace these with your ACTUAL Twitter (or X) API credentials.
    CONSUMER_KEY = (
        (
            "YOUR_CONSUMER_KEY"
        )  # Replace with "YOUR_CONSUMER_KEY" (API Key)
    )
    CONSUMER_SECRET = (
        "YOUR_CONSUMER_SECRET"
    )  # Replace with "YOUR_CONSUMER_SECRET" (Consumer Secret / API Key Secret)
    _instance = None

    def __new__(cls):
        """
        Override the __new__ method to implement the Singleton design pattern
        for the Tweet class.

        This ensures that only one instance of the Tweet class is created. If
        an instance already exists, it returns the existing instance.
        Otherwise, it creates a new instance, initializes the `oauth`
        attribute to None, and calls the `authenticate` method to set up
        authentication.

        Returns:
            Tweet: The singleton instance of the Tweet class.
        """
        if cls._instance is None:
            print("Creating the Tweet singleton instance")
            cls._instance = super(Tweet, cls).__new__(cls)
            cls._instance.oauth = None
            cls._instance.authenticate()
        return cls._instance

    def authenticate(self):
        """
        Authenticates the user with the Twitter API using OAuth 1.0a.

        This method performs the following steps:
        1. Fetches a request token from Twitter.
        2. Directs the user to authorize the application and obtain a PIN.
        3. Exchanges the PIN for an access token.
        4. Creates an authenticated OAuth1Session for making API requests.

        Attributes:
            self.CONSUMER_KEY (str): The consumer key for the Twitter
            application.
            self.CONSUMER_SECRET (str): The consumer secret for the Twitter
            application.
            self.oauth (OAuth1Session): The authenticated session for making
            API requests.

        Steps:
            - Fetches a request token from Twitter's OAuth endpoint.
            - Prompts the user to visit an authorization URL and provide a PIN.
            - Exchanges the PIN for an access token and secret.
            - Initializes an OAuth1Session with the access token
              for future requests.

        Raises:
            ValueError: If there is an error fetching the request token, likely
                        due to invalid consumer key or secret.

        Returns:
            None
        """
        # Step 1: Get request token
        request_token_url = (
            "https://api.twitter.com/oauth/request_token"
            "?oauth_callback=oob&x_auth_access_type=write"
        )
        oauth = OAuth1Session(
            self.CONSUMER_KEY, client_secret=self.CONSUMER_SECRET
        )
        try:
            fetch_response = oauth.fetch_request_token(request_token_url)
        except ValueError:
            print(
                (
                    "Error fetching request token. "
                    "Check your consumer key and secret."
                )
            )
            return
        resource_owner_key = fetch_response.get("oauth_token")
        resource_owner_secret = fetch_response.get("oauth_token_secret")
        print("Got OAuth token: %s" % resource_owner_key)

        # Step 2: Get authorization from the user
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        # Step 3: Get the access token
        access_token_url = "https://api.twitter.com/oauth/access_token"
        oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=verifier,
        )
        oauth_tokens = oauth.fetch_access_token(access_token_url)
        access_token = oauth_tokens["oauth_token"]
        access_token_secret = oauth_tokens["oauth_token_secret"]

        # Step 4: Create an OAuth1Session for making requests
        self.oauth = OAuth1Session(
            self.CONSUMER_KEY,
            client_secret=self.CONSUMER_SECRET,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret,
        )

    def make_tweet(self, tweet):
        """
        Posts a tweet to Twitter using the provided OAuth authentication.

        Args:
            tweet (str): The content of the tweet to be posted.

        Raises:
            ValueError: If OAuth authentication is not available.
            Exception: If the request to the Twitter API fails, with details
                       about the HTTP status code and error message.

        Returns:
            None: Prints the response status code and the JSON response from
                  the Twitter API if the tweet is posted successfully.
        """
        if self.oauth:
            # Dynamically append a timestamp to ensure uniqueness:
            unique_tweet_text = (
                f"{tweet} (Posted at {datetime.datetime.now().isoformat()})"
            )
            response = self.oauth.post(
                "https://api.twitter.com/2/tweets",
                json={"text": unique_tweet_text},
            )
        else:
            raise ValueError("Authentication failed!")
        if response.status_code != 201:
            raise Exception(
                "Request returned an error: {} {}".format(
                    response.status_code,
                    response.text,
                )
            )
        print(
            "Tweet posted successfully. Response code: {}".format(
                response.status_code
            )
        )
        json_response = response.json()
        print(json.dumps(json_response, indent=4, sort_keys=True))
