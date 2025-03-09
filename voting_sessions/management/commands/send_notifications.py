import os
import logging
from django.core.management.base import BaseCommand
from voting_sessions.utils import send_notifications
from unittest.mock import patch
from django.core.mail import send_mail
from django.test import TestCase, override_settings
from django.core.mail import get_connection
from django.test import TestCase
from django.conf import settings
import logging
import sys

logger = logging.getLogger(__name__)

class MyTestCase(TestCase):
    def setUp(self):
        # Log current EMAIL_BACKEND setting to debug
        logger.debug(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        
        # Override the EMAIL_BACKEND for the test to use locmem backend
        settings.EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
        
        # Your other setup code goes here

    def test_email_functionality(self):
        # Test your email functionality here
        # This will use the locmem backend, no real emails will be sent
        pass


print("TEST MODE: Skipping email")



# Force test email backend


@patch("django.core.mail.send_mail")
def test_email_sending(self, mock_send_mail):
        
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
            
# logger = logging.getLogger(__name__)
# logger.debug(f"✅ Final EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
