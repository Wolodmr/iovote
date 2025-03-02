import os
import logging
from django.core.mail import send_mail
from django.utils.timezone import now, localtime, is_naive, make_aware, get_current_timezone
from datetime import timedelta
from voting_sessions.models import Session 
from unittest.mock import patch
from django.core.mail import send_mail



BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Adjust based on script depth
LOG_FILE_PATH = os.path.join(BASE_DIR, "email_debug.log")
logging.basicConfig(
    filename="email_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def send_notifications():
    """Send email notifications for upcoming voting sessions."""
    cet_now = localtime(now())  
    target_time = cet_now + timedelta(hours=1)  

    sessions = Session.objects.filter(session_start_time__lte=target_time)
    
    logger.debug(f"📌 Found {sessions.count()} sessions for notification")
    print(f"📌 Found {sessions.count()} sessions for notification")  # 🚀 NEW

    if not sessions.exists():
        logger.info("No sessions found for notification.")
        print("❌ No sessions found for notification.")  # 🚀 NEW
        return

    for session in sessions:
        logger.debug(f"📌 Processing session: {session.title} at {session.session_start_time}")
        print(f"📌 Processing session: {session.title} at {session.session_start_time}")  # 🚀 NEW

        subject = f"Voting Session Reminder: {session.title}"
        message = f"The voting session '{session.title}' starts in one hour. Don't forget to participate!"
        recipient_list = [session.creator_email]  

        try:
            logger.info(f"📌 Attempting to send email for session: {session.title}")
            print(f"🚀 Calling send_mail for session: {session.title}")  # 🚀 NEW
            send_mail(subject, message, "postvezha@gmail.com", recipient_list)  # 💡 This should be mocked in the test
            session.email_sent = True  
            session.save()
            logger.info(f"✅ Email sent successfully for session: {session.title}")
        except Exception as e:
            logger.error(f"❌ Error sending email for session: {session.title}: {e}", exc_info=True)
