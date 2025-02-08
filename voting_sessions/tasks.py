# voting_sessions/tasks.py

from celery import shared_task
from .utils import broadcast_message_to_chat
from .models import Session
from datetime import timedelta, datetime
print('tasks.0')

@shared_task
def send_initial_notification(session_id):
    """
    Notify about the start of a session.
    """
    print('inside')
    try:
        print('task1')
        session = Session.objects.get(id=session_id)
        print('task2')
        message = f"🎉 A new voting session '{session.title}' has started!"
        print('task3')
        broadcast_message_to_chat(message)
        print('task4')
    except Session.DoesNotExist:
        print('task5')
        print(f"Session with ID {session_id} not found.")

@shared_task
def send_reminder_notification(session_id):
    """
    Notify one day before voting begins.
    """
    try:
        
        session = Session.objects.get(id=session_id)
        reminder_time = session.session_start_time + timedelta(days=session.choice_duration - 1)
        if datetime.now() >= reminder_time:
            message = f"⏰ Reminder: Voting for '{session.title}' starts tomorrow!"
            broadcast_message_to_chat(message)
    except Session.DoesNotExist:
        print(f"Session with ID {session_id} not found.")
        
def notify_session_start(session):
    # Function implementation
    pass

def schedule_voting_reminder(session):
    # Implementation of the function
    pass

