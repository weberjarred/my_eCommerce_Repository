from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile


# Define an inline admin descriptor for Profile model
# which acts a bit like a singleton for each User.
class ProfileInline(admin.StackedInline):
    """
    ProfileInline is a Django admin inline class that allows the Profile model
    to be displayed and edited inline within the admin interface. It uses a
    stacked layout for displaying the fields of the Profile model.

    Attributes:
        model (Model): The model associated with this inline, which is Profile.
        can_delete (bool): Indicates whether the inline objects can be deleted.
            Set to False to prevent deletion.
        verbose_name_plural (str): The plural name displayed in the admin
            interface for this inline, set to "Profile".
    """
    model = Profile
    can_delete = False
    verbose_name_plural = "Profile"


# Define a new User admin
class CustomUserAdmin(UserAdmin):
    """
    CustomUserAdmin is a subclass of Django's UserAdmin that allows for
    customization of the admin interface for the User model.

    It includes the ProfileInline to display and manage related Profile
    model data directly within the User admin page.
    """
    inlines = (ProfileInline,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
