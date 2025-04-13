import logging
import sys
from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)

print("🚀 Running test_email.py")



try:
    send_mail(
        "Test Email",
        "This is a test email.",
        settings.EMAIL_HOST_USER,
        ["test@example.com"],
        fail_silently=False,
    )
    print("✅ Email sent successfully (unexpected)")
except Exception as e:
    print(f"❌ Email sending failed: {e}")
    logger.error(f"❌ Email sending failed: {e}")
