#voting_sessions/management/commands/test_session.py
from django.core.management.base import BaseCommand
from voting_sessions.models import Session
from datetime import timedelta
from django.utils import timezone

class Command(BaseCommand):
    """Creates a test voting session for development purposes."""

    help = "Creates a test voting session"

    def handle(self, *args, **kwargs):
        try:
            session = Session.objects.create(
                title="Test Voting Session",
                description="It's a test session",
                session_start_time=timezone.now() + timedelta(minutes=10),
                choice_duration=timedelta(days=15),
                voting_duration=timedelta(days=5),
                creator_email="user@example.com",
                invitation_endpoint="http://example.com/invite",
            )
            self.stdout.write(self.style.SUCCESS(f"✅ Successfully created session with ID {session.id}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Failed to create session: {e}"))

            


