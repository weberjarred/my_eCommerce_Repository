from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a user profile when a new user is created.

    This function is triggered after a User model instance is saved. If the
    instance is newly created, it automatically creates a corresponding Profile
    object linked to the user.

    Args:
        sender (type): The model class that sent the signal.
        instance (User): The instance of the User model that was saved.
        created (bool): A boolean indicating whether a new record was created.
        **kwargs: Additional keyword arguments passed by the signal.

    Returns:
        None
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal handler to save the profile associated with a user instance.

    This function checks if the given user instance has an associated
    profile attribute. If the profile exists, it saves the profile.

    Args:
        sender (type): The model class that sent the signal.
        instance (object): The instance of the model that triggered the signal.
        **kwargs: Additional keyword arguments passed by the signal.

    Note:
        This function is typically connected to a Django signal, such as
        post_save, to ensure that the profile is saved whenever the user
        instance is saved.
    """
    if hasattr(instance, "profile"):
        instance.profile.save()
