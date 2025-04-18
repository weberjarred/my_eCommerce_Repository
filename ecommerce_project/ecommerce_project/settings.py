"""
Django settings for ecommerce_project project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "your-secret-key"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps for API functionality
    "rest_framework",
    "rest_framework_xml",
    # Custom apps
    # "accounts",
    "store",
    "products",
    "orders",
    "reviews",
    "accounts.apps.AccountsConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "ecommerce_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Global templates directory;
        # app templates are discovered automatically
        "DIRS": [
            BASE_DIR / "templates",
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "orders.context_processors.cart_item_count",
            ],
        },
    },
]

WSGI_APPLICATION = "ecommerce_project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Database configuration – will be using MySQL Workbench.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        # Switch from sqlite to MySQL
        "NAME": "db_name",  # Replace with your actual DB name
        "USER": "your_db_user",  # Replace with your actual DB user
        "PASSWORD": "your_db_password",  # Replace with your actual DB password
        "HOST": "db_host",  # Replace with your actual DB host
        # (e.g., localhost)
        "PORT": "3306",  # Replace with your actual DB port
        # (e.g., 3306 for MySQL)
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# Password validation with minimum length and common checks
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
        "OPTIONS": {"min_length": 8},
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===== ENABLE FOR REAL EMAIL SENDING !!!!!!!!!! ===== #
# Updated—to send real emails. Use the Gmail SMTP server to send emails.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# ===== ENABLE FOR EMAIL TO CONSOLE SENDING !!!!!!!!!! ===== #
# Email configuration for development – emails will be printed to the console.
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = (
    "your_email@gmail.com"  # Replace with your actual email for testing
)
EMAIL_HOST_PASSWORD = (
    (
        "your_app_specific_password"  # Replace with your app-specific password
    )  # for testing
)
DEFAULT_FROM_EMAIL = "Your Store <your_email@gmail.com>"

# For using Gmail, the settings should be updated like this:

# Django REST Framework settings – allow JSON and XML output.
# Set default permission.
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework_xml.renderers.XMLRenderer",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
}

# Set the login URL for the login_required decorator
LOGIN_URL = "/login/"
# LOGIN_REDIRECT_URL = "/"
