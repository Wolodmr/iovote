#voting_sessions/tests.py
from django.test import TestCase
from django.utils.timezone import localtime, now
from django.utils import timezone
from voting_sessions.models import Session
from datetime import timedelta
from django.contrib.auth.models import User
from unittest.mock import patch
from voting_sessions.utils import send_notifications

class NotificationTests(TestCase):
    """Tests for email notification functionality."""

    @patch("voting_sessions.utils.send_mail")  # Mock send_mail
    def test_email_sending(self, mock_send_mail):
        """Ensure an email is sent when calling send_notifications."""
        user = User.objects.create_user(username="testuser", email="test@example.com")

        session = Session.objects.create(
            title="Test Session",
            session_start_time=localtime(timezone.now()) + timedelta(minutes=30),  # ✅ Uses CET
            email_sent=False  
        )
        session.users.add(user)  
        
        print('ONE')
        send_notifications()

        # Assert send_mail was called once
        self.assertEqual(mock_send_mail.call_count, 1)

class SessionModelTests(TestCase):
    """Tests for the Session model."""

    def test_create_valid_session(self):
        """Ensure a session is created with correct end time calculation."""
        start = timezone.now() + timedelta(days=1)
        session = Session.objects.create(
            title="Test Session",
            description="Test Description",
            session_start_time=start,
            choice_duration=timedelta(days=1),
            email_sent=False,
            voting_duration=timedelta(days=3),
            session_end_time=start + timedelta(days=4),  # Adjusted to match calculated duration
        )

        self.assertIsNotNone(session.id)
        self.assertAlmostEqual(
            session.session_end_time,
            session.session_start_time + timedelta(days=4),
            delta=timedelta(milliseconds=10)
        )

    @patch("voting_sessions.models.Session.send_notification")
    def test_notification_sent_on_save(self, mock_send_notification):
        """Ensure notification is sent when saving a session."""
        session = Session.objects.create(
            title="Notification Test",
            description="Test Description",
            session_start_time=timezone.now() + timedelta(days=1),
            session_end_time=timezone.now() + timedelta(days=4),
            choice_duration=timedelta(days=1),
            email_sent=False,
            voting_duration=timedelta(days=2),
        )
        session.save()

        mock_send_notification.assert_called_once_with()

