#voting_sessions/tasks.py

from django.utils.timezone import now
from django.core.mail import send_mail
from .models import Session
#from datetime import timedelta
from django.apps import apps
from django.conf import settings
from django.utils.timezone import now, timedelta
import logging

logger = logging.getLogger(__name__)

def send_voting_session_notifications():
    Session = apps.get_model("voting_sessions", "Session")

    current_time = now()
    target_time = current_time + timedelta(hours=1)
    upcoming_sessions = Session.objects.filter(
        session_start_time__gte=now(),
        session_start_time__lte=now() + timedelta(hours=1)
    )
    logger.info(f"Current time: {current_time}, Target time: {target_time}")
    logger.info(f"Found {upcoming_sessions.count()} sessions matching condition.")
    for session in upcoming_sessions:
        print(f"Email notification sent for session: {session.title}")
    
    for session in upcoming_sessions:
        subject = f"Voting Session Reminder: {session.title}"
        message = f"The voting session '{session.title}' starts in one hour. Don't forget to participate!"
        recipients = ["postvezha@gmail.com"]  # Replace with actual user emails

        # Fetch the email sender from settings
        # send_mail(subject, message, settings.EMAIL_HOST_USER, recipients)
        print(f"Email sent to {recipients} for session: {session.title}")
        
import os
os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")
        

