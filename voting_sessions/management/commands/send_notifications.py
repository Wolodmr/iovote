import os
import logging
from django.core.management.base import BaseCommand
from voting_sessions.utils import send_notifications
from unittest.mock import patch
from django.core.mail import send_mail

print("TEST MODE: Skipping email")

@patch("django.core.mail.send_mail")
def test_email_sending(self, mock_send_mail):
        mock_send_mail.return_value = 1  # Simulate a successful send
        
        # Now call the function that triggers email sending
        result = send_mail(
            'Test Subject',
            'Test Message',
            'from@example.com',
            ['to@example.com']
        )
        
        # Assert that send_mail was called and returned success
        self.assertEqual(result, 1)
        mock_send_mail.assert_called_once()  

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Adjust based on script depth
LOG_FILE_PATH = os.path.join(BASE_DIR, "email_debug.log")

class Command(BaseCommand):
    help = "Send email notifications for upcoming voting sessions"

    def handle(self, *args, **kwargs):
        logger.info("📢 Running send_notifications command...")
        try:
            send_notifications()
            logger.info("✅ Notifications sent successfully.")
        except Exception as e:
            logger.error(f"❌ Error sending notifications: {e}", exc_info=True)  # Logs full error details
            
import os
os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
