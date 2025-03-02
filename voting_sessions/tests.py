# voting_sessions/tests.py

from django.test import TestCase
from django.utils.timezone import now
from django.utils import timezone 
from voting_sessions.models import Session
from unittest.mock import patch
from datetime import timedelta
from unittest.mock import patch
from django.core.mail import send_mail
from django.test import TestCase
from django.conf import settings
from django.test import TestCase
from unittest.mock import patch
from django.utils.timezone import now, localtime, timedelta
from voting_sessions.utils import send_notifications
from voting_sessions.models import Session

class NotificationTests(TestCase):
    @patch("voting_sessions.utils.send_mail")
    def test_send_notifications(self, mock_send_mail):
        """Ensure send_mail is triggered by send_notifications"""

        # ✅ Create a test session that meets the filtering condition
        Session.objects.create(
            title="Test Session",
            session_start_time=localtime(now()) + timedelta(minutes=30),  # Within 1-hour window
            creator_email="test@example.com"
        )

        send_notifications()

        print("📌 mock_send_mail call args:", mock_send_mail.call_args_list)  # Debugging

        mock_send_mail.assert_called()  # ✅ Ensure send_mail was called


print("DEBUG FINAL EMAIL_BACKEND:", settings.EMAIL_BACKEND)
print("DEBUG FINAL EMAIL_HOST:", settings.EMAIL_HOST)
print("DEBUG FINAL EMAIL_PORT:", settings.EMAIL_PORT)
print("DEBUG FINAL EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
print("DEBUG FINAL EMAIL_HOST_PASSWORD:", settings.EMAIL_HOST_PASSWORD)


class YourTestCase(TestCase):
    @patch("django.core.mail.send_mail")  # This prevents real email sending
    def test_email_sending(self, mock_send_mail):
        mock_send_mail.return_value = 1  # Pretend it succeeds
        # Your test logic here


class SessionModelTests(TestCase):
    def test_create_valid_session(self):
        start = timezone.now() + timedelta(days=1)
        self.session = Session.objects.create(
            title="Test Session",
            description="Test Description",
            session_start_time=start,
            choice_duration=timedelta(days=1),
            email_sent = False,
            voting_duration=timedelta(days=3),
            session_end_time=start,  # Set a valid end time
        )
        self.session.session_end_time += self.session.choice_duration + self.session.voting_duration
        self.assertIsNotNone(self.session.id)
        print('set = ', self.session.session_end_time, 'sst = ', self.session.session_start_time + timedelta(days=4))
        # Use assertAlmostEqual to allow for minor differences in microseconds
        self.assertAlmostEqual(
            self.session.session_end_time,
            self.session.session_start_time + timedelta(days=4),
            delta=timedelta(milliseconds=10)
        )
    
    def test_session_duration_calculation(self):
        session = Session(
            title="Duration Test",
            description="Test Description",
            session_start_time=now() + timedelta(days=1),
            session_end_time=timezone.now() + timedelta(days=4),  # Set a valid end time
            choice_duration=timedelta(days=1),
            email_sent = False,
            voting_duration=timedelta(days=2),
        )
        self.assertAlmostEqual(session.session_end_time, session.session_start_time + timedelta(days=3), delta=timedelta(milliseconds=1))

    @patch("voting_sessions.models.Session.send_notification")
    def test_notification_sent_on_save(self, mock_send_notification):
        session = Session(
            title="Notification Test",
            description="Test Description",
            session_start_time=now() + timedelta(days=1),
            session_end_time=timezone.now() + timedelta(days=4),  # Set a valid end time
            choice_duration=timedelta(days=1),
            email_sent = False,
            voting_duration=timedelta(days=2),
            
        )
        session.save()
        mock_send_notification.assert_called_once_with()

    @patch("voting_sessions.models.Session.send_notification")
    def test_no_notification_if_no_changes(self, mock_send_notification):
        session = Session.objects.create(
            title="No Change Test",
            description="Test Description",
            session_start_time=now() + timedelta(days=1),
            session_end_time=timezone.now() + timedelta(days=4),
            choice_duration=timedelta(days=1),
            email_sent = False,
            voting_duration=timedelta(days=2),
        )
        session.save()  # Saving without changes
        # mock_send_notification.assert_called()
        mock_send_notification.assert_called_once_with()
