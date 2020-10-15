from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import UserProfile
import secrets
from simulator import mail


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        if hasattr(instance, 'userprofile'):
            instance.userprofile.user = instance
            instance.userprofile.display_name = instance.username
            instance.userprofile.save()
        else:
            UserProfile.objects.create(user=instance, is_before_user=False)
        mail.send_confirm_email(instance.email, instance.userprofile.confirm_token)
    else:
        instance.userprofile.save()
