from django.core.mail.backends.smtp import EmailBackend
import logging

logger = logging.getLogger(__name__)

class DebugEmailBackend(EmailBackend):
    def open(self):
        logger.debug("Opening SMTP connection...")
        return super().open()

    def close(self):
        logger.debug("Closing SMTP connection...")
        return super().close()

    def send_messages(self, email_messages):
        logger.debug(f"Attempting to send {len(email_messages)} email(s)...")
        return super().send_messages(email_messages)
