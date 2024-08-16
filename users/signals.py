# users/signals.py

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, AdPreferences

logger = logging.getLogger(__name__)

@receiver(post_save, sender=CustomUser)
def create_ad_preferences(sender, instance, created, **kwargs):
    # Log to debug
    logger.debug(f"Signal received for user: {instance.email}, role: {instance.role}, created: {created}")

    if created:
        if instance.role == 'merchant':
            # Log before creating AdPreferences
            logger.debug(f"Creating AdPreferences for user: {instance.email}")
            AdPreferences.objects.get_or_create(user=instance)
        else:
            # Log if role is not 'merchant'
            logger.debug(f"AdPreferences not created for user: {instance.email} with role: {instance.role}")
