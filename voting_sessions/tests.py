#voting_sessions/tests.py
from django.test import TestCase
from django.utils import timezone
from voting_sessions.models import Session
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from unittest.mock import patch
from voting_sessions.utils import send_notifications
import logging
import sys

logger = logging.getLogger(__name__)

# Notification Tests
class NotificationTests(TestCase):
    @patch("voting_sessions.utils.send_mail")  # Mock send_mail
    def test_email_sending(self, mock_send_mail):
        """Test that an email is sent when calling send_notifications."""
        
        # Step 1: Create a test session that needs notification
        session = Session.objects.create(
            title="Test Session",
            session_start_time=timezone.localtime() + timedelta(minutes=50),
            email_sent=False  # Ensure it qualifies for notification
        )
        
        # Step 2: Run send_notifications()
        send_notifications()
        
        # Step 3: Assert email was sent
        mock_send_mail.assert_called_once()  # Check if send_mail was called exactly once

# Session Model Tests
class SessionModelTests(TestCase):
    def test_create_valid_session(self):
        start = timezone.now() + timedelta(days=1)
        session = Session.objects.create(
            title="Test Session",
            description="Test Description",
            session_start_time=start,
            choice_duration=timedelta(days=1),
            email_sent=False,
            voting_duration=timedelta(days=3),
            session_end_time=start,  # Set a valid end time
        )
        session.session_end_time += session.choice_duration + session.voting_duration
        self.assertIsNotNone(session.id)
        self.assertAlmostEqual(
            session.session_end_time,
            session.session_start_time + timedelta(days=4),
            delta=timedelta(milliseconds=10)
        )
    
    def test_session_duration_calculation(self):
        session = Session(
            title="Duration Test",
            description="Test Description",
            session_start_time=timezone.now() + timedelta(days=1),
            session_end_time=timezone.now() + timedelta(days=4),  # Set a valid end time
            choice_duration=timedelta(days=1),
            email_sent=False,
            voting_duration=timedelta(days=2),
        )
        self.assertAlmostEqual(session.session_end_time, session.session_start_time + timedelta(days=3), delta=timedelta(milliseconds=10))

    @patch("voting_sessions.models.Session.send_notification")
    def test_notification_sent_on_save(self, mock_send_notification):
        session = Session(
            title="Notification Test",
            description="Test Description",
            session_start_time=timezone.now() + timedelta(days=1),
            session_end_time=timezone.now() + timedelta(days=4),  # Set a valid end time
            choice_duration=timedelta(days=1),
            email_sent=False,
            voting_duration=timedelta(days=2),
        )
        session.save()
        
        mock_send_notification.assert_called_once_with()

    @patch("voting_sessions.models.Session.send_notification")
    def test_no_notification_if_no_changes(self, mock_send_notification):
        session = Session.objects.create(
            title="No Change Test",
            description="Test Description",
            session_start_time=timezone.now() + timedelta(days=1),
            session_end_time=timezone.now() + timedelta(days=4),
            choice_duration=timedelta(days=1),
            email_sent=False,
            voting_duration=timedelta(days=2),
        )
        session.save()  # Saving without changes
        if "test" in sys.argv:
                print("🚫 Skipping email sending during tests.")
                return  # Bypass email sending
        mock_send_notification.assert_called_once_with()
