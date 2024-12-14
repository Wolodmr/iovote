from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from voting_sessions.models import Session

class SimpleTest(TestCase):
    def test_session_creation(self):
        # Ensure session_start_time is aware
        session_start_time = timezone.now() + timedelta(days=1)  # Make this a valid future time
        
        session = Session.objects.create(
            title="Test Session",
            description="Test description",
            session_start_time=session_start_time,
            choice_duration=timedelta(days=1),
            voting_duration=timedelta(days=1)
        )
        
        self.assertEqual(session.title, "Test Session")
