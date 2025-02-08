from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Session
from .tasks import send_initial_notification, send_reminder_notification
from datetime import timedelta
from django.conf import settings

@receiver(post_save, sender=Session)
def handle_session_creation(sender, instance, created, **kwargs):
    if created:
        # Send the initial notification
        print('signals.created')
        send_initial_notification.delay(session_id=1)
        print('1')
        # Schedule the reminder notification
        reminder_eta = instance.session_start_time + instance.choice_duration - timedelta(days=1)
        send_reminder_notification.apply_async(kwargs={'session_id': instance.id}, eta=reminder_eta)
    if settings.DEBUG:
        send_reminder_notification(instance.id)  # Direct execution in DEBUG mode
    else:
        send_reminder_notification.apply_async(kwargs={'session_id': instance.id})

