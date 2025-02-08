#vote/tasks.py

from celery import shared_task

@shared_task
def example_task():
    # Task logic here
    print("Processing vote...")
    return "Task executed"

