# celery_worker/tasks.py

from celery import shared_task
from vote.models import Vote  # Ensure this import works

@shared_task
def example_task(vote_id):
    try:
        vote = Vote.objects.get(id=vote_id)
        print(f"Processing vote {vote}")
        # Perform any task-related logic here
    except Vote.DoesNotExist:
        print(f"Vote with id {vote_id} does not exist")
