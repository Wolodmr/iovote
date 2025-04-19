#voting_sessions/management/commands/send_notifications.py
import logging
from django.core.management.base import BaseCommand
from voting_sessions.utils import send_notifications

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    """Django management command to send email notifications for upcoming voting sessions."""

    help = "Send email notifications for upcoming voting sessions"

    def handle(self, *args, **kwargs):
        logger.info("📢 Running send_notifications command...")

        try:
            print('SEND')
            send_notifications()
            logger.info("✅ Notifications sent successfully.")
        except Exception as e:
            logger.error(f"❌ Error sending notifications: {e}", exc_info=True)
