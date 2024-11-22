import logging

logger = logging.getLogger(__name__)

logger.debug("Debugging tasks.py initialization")
from celery import shared_task
logger.debug("Debugging tasks.py initialization1")
from datetime import timedelta
from .models import Session
from .utils import broadcast_message_to_chat  # Assuming this is a custom function

@shared_task
def send_initial_notification(session_id):
    session = Session.objects.get(id=session_id)
    message = (
        f"📢 **The Voting Session has Started!** Explore the options and prepare to vote. "
        f"Voting begins on {session.session_start_time + timedelta(days=session.choice_duration)}."
    )
    broadcast_message_to_chat(message)

@shared_task
def send_reminder_notification(session_id):
    session = Session.objects.get(id=session_id)
    message = (
        f"⏳ **Voting Reminder!** The voting session '{session.title}' begins tomorrow at "
        f"{session.session_start_time + timedelta(days=session.choice_duration)}. Be ready to cast your vote!"
    )
    broadcast_message_to_chat(message)
