#voting_sessions/utils.py
import logging
from datetime import timedelta
from django.core.mail import send_mail, get_connection
from django.utils.timezone import localtime, now
from django.conf import settings
from django.urls import reverse
from django.utils.html import strip_tags
from voting_sessions.models import Session
from django.contrib.auth import get_user_model
import logging
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.contrib.auth import get_user_model
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="email_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def send_notifications():
    print('STARTED')
    """Send email notifications for upcoming voting sessions."""
    cet_now = now()
    target_time = cet_now + timedelta(hours=1)

    logger.info(f" Checking sessions between {cet_now} and {target_time}")

    sessions = Session.objects.filter(
        email_sent=False,
        session_start_time__range=(cet_now, target_time)
    ).prefetch_related("users")

    if not sessions.exists():
        print('NO')
        logger.info("No sessions found for notification.")
        return

    session_ids_to_update = []

    for session in sessions:
        voting_start_time = session.voting_start_time

        duration = session.choice_duration
        if duration < timedelta(hours=1):
            choice_duration_display = f"{int(duration.total_seconds() // 60)} minutes"
        elif duration < timedelta(days=1):
            choice_duration_display = f"{int(duration.total_seconds() // 3600)} hours"
        else:
            choice_duration_display = f"{int(duration.days)} days"

        subject = session.title
        voting_url = f"{settings.SITE_URL}{reverse('voting_sessions:session_invite', kwargs={'session_uuid': session.uuid})}"

        html_message = f"""
        <html>
          <body style=\"font-family: Arial, sans-serif; line-height: 1.6;\">
            <h2 style=\"color: #2e6c80;\">🗳️ Invitation to Vote: {session.title}</h2>
            <p><strong>Description:</strong><br>{session.description}</p>

            <p><strong>🗓️ Start Time:</strong> {localtime(session.session_start_time).strftime('%Y-%m-%d %H:%M %Z')}</p>
            <p><strong>⏳ Choice Duration:</strong> {choice_duration_display}</p>
            <p style=\"margin-left: 1em; font-style: italic;\">
              This is the period suggested by the session creator for voters to recall or explore relevant information, 
              to reflect, or to discuss the subject before voting. The voting process will start exactly when this period ends.
            </p>

            <p><strong>🗓️ Voting Time Starts:</strong> {localtime(voting_start_time).strftime('%Y-%m-%d %H:%M %Z')}</p>
            <p><strong>⏱️ End Time:</strong> {localtime(session.session_end_time).strftime('%Y-%m-%d %H:%M %Z')}</p>

            <p><a href=\"{voting_url}\" style=\"display: inline-block; padding: 10px 15px; background-color: #2e6c80; color: white; text-decoration: none; border-radius: 5px;\">Cast Your Vote</a></p>
          </body>
        </html>
        """

        plain_message = strip_tags(html_message)
        recipient_list = []
        User = get_user_model()
        for user in User.objects.filter(email__gt=''):
             recipient_list.append(user.email)
            
        #recipient_list = list(session.users.values_list("email", flat=True).filter(email__gt=""))

        if not recipient_list:
            logger.warning(f" No valid email recipients for session: {session.title}")
            continue

        try:
            with get_connection(backend=settings.EMAIL_BACKEND) as connection:
                
                send_mail(subject, plain_message, settings.EMAIL_HOST_USER, recipient_list, html_message=html_message, connection=connection)
            session_ids_to_update.append(session.id) 
            logger.info(f" Email sent successfully for session: {session.title}")
        except Exception as e:
            logger.error(f" Error sending email for session '{session.title}': {e}", exc_info=True)

    if session_ids_to_update:
        Session.objects.filter(id__in=session_ids_to_update).update(email_sent=True)
