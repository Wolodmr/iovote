#voting_sessions/utils.py
import os
import logging
import sys
from datetime import timedelta
from django.core.mail import send_mail, get_connection
from django.utils.timezone import localtime, now
from django.conf import settings
from voting_sessions.models import Session

# Logger configuration
logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="email_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_notifications():
    """Send email notifications for upcoming voting sessions."""
    
    cet_now = localtime(now())
    target_time = cet_now + timedelta(hours=1)
    
    sessions = Session.objects.filter(session_start_time__lte=target_time)
    print(sessions)
    for session in Session.objects.all():
        print(session, target_time)
    logger.debug(f"Found {sessions.count()} sessions for notification")
    
    if not sessions.exists():
        logger.info("No sessions found for notification.")
        return
    
    for session in sessions:
        subject = f"Voting Session Reminder: {session.title}"
        message = (
            f"The voting session '{session.title}' starts in one hour. "
            "Don't forget to participate!"
        )
        recipient_list = [session.creator_email]
        
        try:
            connection = get_connection(backend=settings.EMAIL_BACKEND)
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, recipient_list, connection=connection
            )
            session.email_sent = True
            session.save()
            logger.info(f"Email sent successfully for session: {session.title}")
        except Exception as e:
            logger.error(f"Error sending email for session: {session.title}: {e}", exc_info=True)
