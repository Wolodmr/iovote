from django.core.management.base import BaseCommand
from voting_sessions.models import Session
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Creates a test voting session'

    def handle(self, *args, **kwargs):
        try:
            session = Session.objects.create(
                title='Test Voting Session',
                description="It's a test session",
                session_start_time= timezone.now() + timedelta(minutes=10),
                choice_duration=timedelta(days=15),
                voting_duration=timedelta(days=5),
                creator_email="user@example.com",  # Make sure to provide an email
                invitation_endpoint="http://example.com/invite",  # Provide the endpoint URL
            )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to create session: {e}"))
        else:
            self.stdout.write(self.style.SUCCESS(f'Successfully created session with ID {session.id}'))
        

