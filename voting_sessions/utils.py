import logging
from datetime import timedelta
from django.core.mail import send_mail, get_connection
from django.utils.timezone import localtime, now
from django.conf import settings
from django.urls import reverse
from voting_sessions.models import Session

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

    logger.info(f"🔍 Checking sessions between {cet_now} and {target_time}")

    # ✅ Get only relevant sessions & prefetch users efficiently
    sessions = Session.objects.filter(
        email_sent=False,
        session_start_time__range=(cet_now, target_time)
    ).prefetch_related("users")  # Keep prefetch_related if `users` is ManyToMany

    if not sessions.exists():
        logger.info("No sessions found for notification.")
        return

    session_ids_to_update = []  # Collect IDs for bulk update

    for session in sessions:
        subject = f"Voting Session Reminder: {session.title}"
        voting_url = f"{settings.SITE_URL}{reverse('voting_sessions:session_invite', kwargs={'session_uuid': session.uuid})}"
        message = f"The voting session '{session.title}' starts in one hour. Don't forget to participate!\n\nVote here: {voting_url}"

        # ✅ Fetch emails efficiently
        recipient_list = list(session.users.values_list("email", flat=True).filter(email__gt=""))

        logger.info(f"📩 Sending emails for session '{session.title}' to {len(recipient_list)} recipients.")

        if not recipient_list:
            logger.warning(f"⚠️ No valid email recipients for session: {session.title}")
            continue  # Skip session if no valid emails

        try:
            with get_connection(backend=settings.EMAIL_BACKEND) as connection:
                send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, connection=connection)

            session_ids_to_update.append(session.id)  # Collect session ID

            logger.info(f"✅ Email sent successfully for session: {session.title}")
        except Exception as e:
            logger.error(f"❌ Error sending email for session '{session.title}': {e}", exc_info=True)

    # ✅ Bulk update email_sent field for all processed sessions
    if session_ids_to_update:
        Session.objects.filter(id__in=session_ids_to_update).update(email_sent=True)
