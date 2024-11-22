from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from datetime import timedelta
from .models import Session
from .tasks import send_reminder_notification, send_initial_notification

@receiver(post_save, sender=Session)
def schedule_notifications(sender, instance, created, **kwargs):
    if created:
        # First notification: At session_start_time
        send_initial_notification.apply_async(
            args=[instance.id], eta=instance.session_start_time
        )

        # Second notification: A day before voting starts
        reminder_time = instance.session_start_time + timedelta(
            days=instance.choice_duration - 1
        )
        send_reminder_notification.apply_async(
            args=[instance.id], eta=reminder_time
        )
