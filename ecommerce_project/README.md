# Project Documentation

# eCommerce Platform Application

The project is a multi-vendor eCommerce application built using Django. Its main objective is to allow vendors to manage products within their own stores while enforcing permissions so that vendors can only create, edit, or delete products associated with their account. For example, if a vendor attempts to edit or delete a product that belongs to another vendor, they receive an "Access Denied" message or a 403 error.

**Overview and Frameworks:**

- **Framework:** Django is the core web framework used in the project.

- **Languages & Tools:** Python for backend logic; Django’s templating engine for frontend views; built-in Django authentication combined with custom decorators for access control.

- **Additional Integrations:** The project includes functionality (planned for Phase 2) to tweet newly created products via an integrated Tweet module.

**Key Functionality:**

- **Product Views:** The application includes several views for listing products, viewing product details, and allowing vendors to create, update, or delete products.

- **Permission Control:** Custom decorators (e.g., vendor_required) and explicit permission checks in views ensure that only the owner of a product’s store can modify it.

- **User Feedback:** Uses Django’s messages framework to provide success or error notifications.

- **Data Management:** The Django shell can be used to inspect vendor and store data (for instance, retrieving a vendor’s ID using Django’s ORM).

**Usage Examples and Configuration:**

- **Creating a Product:** Vendors log in, access their designated store, and use the product form to add new products.

- **Editing/Deleting Products:** The code restricts access by comparing the product’s associated vendor with the logged-in user.

- **Prerequisites:** A working Django environment, Django’s built-in User and authentication system, a properly configured database, and basic familiarity with running shell commands (e.g., python manage.py shell) for administration tasks.

This concise setup forms the foundation of the eCommerce platform, ensuring secure, vendor-specific product management. This modular eCommerce Web Application built with Python showcases CRUD capabilities, a responsive design through Bootstrap, and a modular project structure, and it employs unit testing following the AAA pattern. Every template incorporates semantic HTML elements (header, section, article, footer) and Bootstrap classes to achieve a responsive and polished design. Organised project structure extends to the eCommerce application with a secure RESTful API and also integrates Twitter’s API to tweet when new stores or products are added.

## TESTING

- Testing with Console Email Backend:
  For development purposes, you might want to use the console email backend
  (which prints emails to the console) to bypass SMTP credentials issue.
  This can be found in settings.py.

## BUYER & VENDOR INFORMATION

| Buyer01       |                   |
| ------------- | ----------------- |
| **username:** | JohnDoe           |
| **email:**    | DoeJohn@email.com |
| **password:** | P@55w0Rd4528_DJ   |

| Buyer02       |                    |
| ------------- | ------------------ |
| **username:** | JaneDoe            |
| **email:**    | DoeJane@email.com  |
| **password:** | P@55w0Rd4528_MrsDJ |

| Buyer03       |                     |
| ------------- | ------------------- |
| **username:** | JackGreen           |
| **email:**    | GreenJack@email.com |
| **password:** | G@88w0Rd4948_GJ     |

| Vendor01      |                     |
| ------------- | ------------------- |
| **username:** | JohnApple           |
| **email:**    | AppleJohn@email.com |
| **password:** | P@66w0Rd4528_DJ     |

| Vendor02      |                      |
| ------------- | -------------------- |
| **username:** | JohnBanana           |
| **email:**    | BananaJohn@email.com |
| **password:** | P@66w0Rd4528_BJ      |

| Vendor03      |                     |
| ------------- | ------------------- |
| **username:** | ChrisHunt           |
| **email:**    | HuntChris@email.com |
| **password:** | CR11w0Rd4537_HC     |

## 1. Project Structure

    django_project__eCommerce/                # Project folder directory
    │
    ├── myVenv/                               # Virtual environment folder
    │
    └── ecommerce_project/                    # Proj. ROOT folder dir. (UPPER / OUTER) proj. dir.
       ├── manage.py                          # Django management script
       ├── README.md                          # Project description
       ├── .flake8                            # Code style configuration
       ├── .pyproject.toml                    # Project configuration (e.g., Black)
       ├── requirements.txt                   # Project dependencies
       ├── .gitignore                         # Git ignore file
       ├── db.sqlite3                         # Development database (or MariaDB in production)
       │
       ├── ecommerce_project/                 # Core (INNER) proj. folder (settings and configuration)
       │  ├── __init__.py
       │  ├── settings.py                     # Glob. settings (incl. installed apps, static files, etc.)
       │  ├── urls.py                         # Root URL dispatcher
       │  ├── wsgi.py
       │  ├── home.py
       │  └── asgi.py
       │
       │
       │ ==== # Folders for Django apps START here # ====
       │
       ├── accounts/                          # New app for authentication and user management
       │  ├── migrations/
       │  │  └── __init__.py
       │  ├── __init__.py
       │  ├── admin.py
       │  ├── apps.py                         # User authentication, registration
       │  ├── models.py                       # (Optional) Extended user profiles
       │  ├── forms.py                        # User authentication and password management.
       │  ├── views.py                        # Views for registration, login, logout, password management etc.
       │  ├── urls.py                         # URLs specific to authentication
       │  ├── tests.py                        # Tests that cover user reg., login, and password reset
       │  ├── context_processors.py
       │  ├── signals.py                      # Creates a Profile instance whenever a new User is created
       │  ├── decorators.py                   # Secure vendor-only/buyer-only functionality preventing UI bypass attempts
       │  ├── static/
       │  │ └── accounts/
       │  │    ├── css/
       │  │    │  └── styles.css
       │  │    └── js/
       │  │       └── scripts.js
       │  ├── templates/
       │  │  └── accounts/
       │  │     ├── register.html             # User registration form
       │  │     ├── login.html                # User Login form
       │  │     ├── password_reset.html       # Form to request a password reset
       │  │     └── reset_password.html       # Form to set a new password after token validation
       │  │
       │  │
       │  └── templatetags/                   # Custom template tags
       │     ├── __init__.py
       │     └── group_tags.py
       │
       │
       │
       ├── store/                             # New app for vendor store management
       │  ├── migrations/
       │  │  └── __init__.py
       │  ├── __init__.py
       │  ├── admin.py
       │  ├── apps.py                         # Handle tweet new store creations
       │  ├── models.py                       # Store model and related logic
       │  ├── forms.py                        # Store creation/edit forms, vendor store management forms
       │  ├── views.py                        # Views dashboard—for creating, editing, deleting stores, store products
       │  ├── urls.py                         # URL patterns for store management
       │  ├── tests.py                        # Verify vendor functionality, creating, editing, and deleting a store.
       │  ├── serializers.py
       │  ├── api_views.py                    # Endpoints for creating a new store
       │  ├── api_urls.py                     # Endpoints for listing, creating a stores, retrieving vendor stores
       │  ├── static/
       │  │  └── store/
       │  │     ├── css/
       │  │     │  └── styles.css
       │  │     └── js/
       │  │        └── scripts.js
       │  └── templates/
       │     └── store/
       │        ├── store_form.html            # Create/edit store
       │        ├── store_delete_confirm.html  # Confirm to delete a store by a vendor
       │        ├── store_products.html        # Template to Display the Store’s Products
       │        ├── vendor_dashboard.html      # Dashboard for vendor users
       │        └── vendor_products.html       # Display for vendor users
       │
       │
       ├── products/                          # New app for product management
       │  ├── migrations/
       │  │ └── __init__.py
       │  ├── __init__.py
       │  ├── admin.py
       │  ├── apps.py                         # Product-related logic
       │  ├── models.py                       # Product model and (optionally) review model
       │  ├── forms.py                        # Product forms, and possibly review forms
       │  ├── views.py                        # Views for product listing, detail, CRUD
       │  ├── urls.py                         # URL patterns for products
       │  ├── tests.py                        # product management functions—creating, updating, and deleting products
       │  ├── serializers.py
       │  ├── api_views.py                    # Endpoints for creating a new product, retrieving products for a store
       │  ├── api_urls.py                     # Endpoints for creating new products, retrieving products for a store
       │  ├── static/
       │  │  └── products/
       │  │     ├── css/
       │  │     │  └── styles.css
       │  │     └── js/
       │  │        └── scripts.js
       │  └── templates/
       │     └── products/
       │        ├── product_list.html            # List products for buyers
       │        ├── product_detail.html          # List products detail for buyers
       │        ├── product_form.html            # Create/edit product
       │        ├── product_delete_confirm.html  # Confirm to delete a product from a store
       │        └── vendor_products.html         # Shows Products by [vendor username]
       │
       ├── orders/                              # New app for cart, checkout, and order processing
       │  ├── migrations/
       │  │  └── __init__.py
       │  ├── __init__.py
       │  ├── admin.py
       │  ├── apps.py                           # Order app config.
       │  ├── models.py                         # Order and OrderItem models
       │  ├── views.py                          # Cart view, checkout view, invoice generation
       │  ├── urls.py                           # URL patterns for orders
       │  ├── tests.py                          # Tests covering cart functionality and the checkout process
       │  ├── context_processors.py
       │  ├── static/
       │  │  └── orders/
       │  │     ├── css/
       │  │     │  └── styles.css
       │  │     └── js/
       │  │        └── scripts.js
       │  └── templates/
       │     └── orders/
       │        ├── cart.html                   # Shopping cart view
       │        ├── checkout.html               # Checkout view
       │        └── invoice_email.html          # HTML for invoice email (sent on checkout)
       │
       ├── reviews/                             # (Optional) New app solely for reviews functionality
       │  ├── migrations/
       │  │  └── __init__.py
       │  ├── __init__.py
       │  ├── admin.py
       │  ├── apps.py                           # Review functionality app config.
       │  ├── models.py                         # Review model if separated from products
       │  ├── forms.py                          # Review submission forms
       │  ├── views.py                          # Views for adding and listing reviews
       │  ├── urls.py                           # URL patterns for reviews
       │  ├── tests.py                          # Verify that a buyer can submit a review for a product
       │  ├── serializers.py
       │  ├── api_views.py                      # Review endpoints
       │  ├── api_urls.py                       # Endpoints relating to reviews
       │  ├── static/
       │  │  └── reviews/
       │  │     ├── css/
       │  │     │  └── styles.css
       │  │     └── js/
       │  │        └── scripts.js
       │  └── templates/
       │     └── reviews/
       │        ├── add_review.html
       │        └── review_list.html
       │
       │ ==== # Folders for Django apps END here # ====
       │
       │
       │
       ├── functions/                           # Package for third-party integrations
       │  ├── __init__.py                       # Makes this a Python package
       │  └── tweet.py                          # Contains the Tweet class for Twitter API integration
       │
       │
       ├── templates/                           # Global templates (if any)
       │  ├── base.html                         # Main Base template with Bootstrap & semantic HTML
       │  └── home.html                         # Creates a dedicated landing page
       │
       └── static/                              # Global static assets (if any)
          ├── css/
          │  └── styles.css
          ├── js/
          └── images/

    OPTIONAL:
    For .flake8:
    [flake8]
    max-line-length = 79
    exclude = .git,**pycache**,tests,venv
    ignore = E203, E266, W503

    OPTIONAL:
    For .pyproject.toml:
    [tool.black]
    line-length = 79

## 2. Setup Instructions

1.  **Create 'django_project\_\_eCommerce' folder in file explorer.**

        "C:\...\django_project__eCommerce" => project folder dir

2.  **Create a virtual environment - while in project folder dir**

        Type: 'python -m venv myVenv' into vs code terminal

    2.1. **Activate virtual environment**

        Type: 'source myVenv/Scripts/activate' into vs code terminal, then
        Type: 'pip freeze' into the vs code term.

3.  **Install django - still while in project folder dir**

        Type: 'pip install django' into the vs code terminal, then
        Type: 'pip freeze' into the vs code term.

4.  **Create a new django project and application**

    4.1. **Create a new django project:**

        Type: 'django-admin startproject ecommerce_project' into vs code term, while still in proj. folder dir

    4.2. **Change directory to proj ROOT dir**

        Type: 'cd ecommerce_project' into vs code term

    4.3. **Create a new Django application:**

        Type: 'django-admin startapp accounts' into vs code term
        Type: 'ls' into vs code term
        -----→ repeat 4.3 for other applications created.

5.  **Run initial database migrations to set up the database tables:**

        Type: 'python manage.py migrate' into the vs code term

6.  **Create a superuser to access the Django admin interface:**

        Type: 'python manage.py createsuperuser' into the vs code term, then,
        Fill in: username (James --this is a fictitious username), email (rrrr@rrrr.com), password (1234 --this is a fictitious password)

7.  **Start the Django development server:**

        Type: 'python manage.py runserver' into the vs code term, then follow the http://... link in term

8.  **Create the necessary subfolders and modules where needed within the proj folder dir or proj root dir**

9.  **Edit and populate the different modules and subfolders**

10. **Install flake8:**

        Type: 'pip install flake8' into the vs code term and create and populate the .flake8 file.

11. **Install Black:**

        Type: 'pip install black' into the vs code term

12. **Perform black and flake8 PEP 8 standards. >>> Use prettier with caution on HTML, CSS, JavaScript. It causes app errors**

13. **Install MySQL on your local machine, define host, port, username, and password accordingly.**

        Then, connect to your MySQL server.

14. **Run Migrations:**

        Open your terminal and execute the following commands in your project’s ROOT directory:
        Type: 'python manage.py makemigrations'
        'python manage.py migrate' into the vs code term

15. **Restart Your Development Server:**

        Type: 'python manage.py runserver' into the vs code term, then follow the http://... link in term

16. **Use your application and check if it works.**

17. **Generate requirements.exe file:**

        Type: 'pip freeze > requirements.txt' into vs code term, while in proj root dir.

    17.1. **Always keep the requirements.txt file updated to include all necessary dependencies.**

18. **Generate README.md file.**

        NOTE: Perform migrations to ensure that any new changes are reflected in the database, and restart the development server to test your application.

    **NOTE:** ALWAYS CHECK THAT YOUR README.md FILE CONTENTS / CHARACTERS ARE DISPLAYED CORRECTLY BEFORE FINAL DEPLOYMENT OF APPLICATION! → The application of flack8 and black can cause display errors.

19. **Install djangorestframework:**

        Type: 'pip install djangorestframework' into the vs code term, while still in the proj root dir.

20. **Install requests_oauthlib.**

        Type: 'pip install requests_oauthlib' in the vs code term, while still in the proj root dir.

21. **Install Postman**

22. **Test GET Endpoints:**

- Test the endpoint that lists all products, set the method to **GET** within Postman.
  Use the URL: 'http://127.0.0.1:8000/api/products/list/' and click send.
  use buyer credentials → you should get a **200 OK** message, under basic auth.

- Test the endpoint that lists logs users in, set the method to **GET** within Postman.
  Use the URL: 'http://127.0.0.1:8000/accounts/login/'
  test using buyer and vendor credentials → you should get a **200 OK** message, under basic auth for both.

- Test the endpoint that lists all stores, set the method to **GET** within Postman.
  Use the URL: 'http://127.0.0.1:8000/api/store/list/'
  use buyer credentials → you should get a **200 OK** message, under basic auth.

  22.1. **Inspect the JSON response in Postman**

  - You should receive **200 OK** message.

23. **Test POST Endpoints:**

- Test the endpoint that creates a new store, set the method to **POST** in Postman.
  Use the URL: 'http://127.0.0.1:8000/api/store/add/', then in the Authorization tab, choose Basic Auth and enter one of your vendor's username and password [JohnApple id=11 (checked using python shell)].

  - In the Body tab, select raw and choose JSON as the type.

    Type:

    ```json
    {
      "vendor": 11,
      "name": "My New Store",
      "description": "We sell awesome products!",
      "logo": null
    }
    ```

    into the field → then click send

    - If successful, you should receive a JSON response with the new store’s data and an HTTP status code of **201**. Thus creates a new store.

- Test the endpoint that adds a new product to a given store, set the method to POST in Postman.
  Use the URL: 'http://127.0.0.1:8000/api/products/add/', then in the Authorization tab, choose Basic Auth and enter one of your vendors username and password [store id=3 (checked using python shell), product id=6 (Checked using python shell—Just chose to next integer after the last integer)].

  - In the Body tab, select raw and choose JSON as the type.

    Type:

    ```json
    {
      "id": 6,
      "store": 3,
      "name": "New Product",
      "description": "Product description",
      "price": "2958.99",
      "stock": 52,
      "image": null
    }
    ```

    into the field → then click send

    - If successful, you should receive a JSON response with the new store’s data and an HTTP status code of **201**. Thus a new product has / will been added.

24. **Run tests once again. i.e.**

        Type: 'python manage.py test' and 'python manage.py test --verbosity 2' into the vs code term.

## 3. Frequently used commands

    django-admin startproject ecommerce_project

    ecommerce_project

    django-admin startapp shop

    python manage.py migrate

    python manage.py createsuperuser

    python manage.py runserver

    python manage.py makemigrations
    python manage.py migrate

    python manage.py makemigrations && python manage.py migrate

    pip freeze > requirements.txt

This command recursively searches your project directory for any folders named pycache and deletes them.

    find . -type d -name "__pycache__" -exec rm -rf {} +

### 3.1. Frequently used _Test Commands_

    python manage.py test

    python manage.py test --verbosity 2

    python manage.py test orders -v 3 (app-specific)

    python manage.py test orders (app-specific)

    http://127.0.0.1:8000/admin/

---

---
