import logging
from datetime import timedelta
from django.core.mail import send_mail, get_connection
from django.utils.timezone import localtime, now
from django.conf import settings
from voting_sessions.models import Session
from django.urls import reverse

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
    
    print(f"🔍 Current time: {cet_now}")
    print(f"⏳ Target time (1 hour ahead): {target_time}")

    # Print all session times
    all_sessions = Session.objects.all()
    print("📅 All sessions in DB:")
    for s in all_sessions:
        print(f"- {s.title}: {s.session_start_time} (Email Sent: {s.email_sent})")

    sessions = Session.objects.filter(session_start_time__lte=target_time, session_start_time__gte=cet_now)

    if not sessions.exists():
        logger.info("No sessions found for notification.")
        return
    
    for session in sessions:
        subject = f"Voting Session Reminder: {session.title}"
        voting_url = f"{settings.SITE_URL}{reverse('voting_sessions:session_invite', kwargs={'session_uuid': session.uuid})}"

        message = f"The voting session '{session.title}' starts in one hour. Don't forget to participate!\n\nVote here: {voting_url}"

        recipient_list = [user.email for user in session.users.all() if user.email]
        print(session.title)
        print(f"Recipient List: {recipient_list}")
        print(f"Generated voting URL: {voting_url}")

        
        if not recipient_list:
            logger.warning(f"No valid email recipients for session: {session.title}")
            continue  # Skip this session if no emails

        try:
            with get_connection(backend=settings.EMAIL_BACKEND) as connection:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, connection=connection)
            session.email_sent = True
            session.save()
            logger.info(f"Email sent successfully for session: {session.title}")
        except Exception as e:
            logger.error(f"Error sending email for session '{session.title}': {e}", exc_info=True)
