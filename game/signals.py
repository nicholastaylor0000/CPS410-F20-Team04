from django.db.models.signals import post_save
from .models import GameResult
from django.dispatch import receiver
from .models import UserProfile
import secrets

@receiver(post_save, sender=GameResult)
def create_gameresult(sender, instance, created, **kwargs):
    if created:
        if instance.copilot:
            copilot = instance.copilot.display_name
        else:
            copilot = ''
