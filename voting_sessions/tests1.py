from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone
from django.test import TestCase
from django.core.exceptions import ValidationError
from voting_sessions.models import Session


@patch('voting_sessions.tasks.send_reminder_notification.apply_async')  # Mock send_reminder_notification
@patch('voting_sessions.tasks.send_initial_notification.delay')  # Mock send_initial_notification
class SessionEdgeCaseTests(TestCase):

    def test_boundary_times(self, mock_send_initial, mock_send_reminder):
        session_start = timezone.now() - timedelta(hours=1)  # Set past start time
        with self.assertRaises(ValidationError) as context:
            Session.objects.create(
                title="Boundary Test",
                description="Testing boundary times",
                session_start_time=session_start,
                choice_duration=timedelta(hours=2),
                voting_duration=timedelta(hours=2),
            )
        self.assertIn("Session start time cannot be in the past.", str(context.exception))
        mock_send_initial.assert_not_called()
        mock_send_reminder.assert_not_called()

    def test_excessive_combined_duration(self, mock_send_initial, mock_send_reminder):
        future_start_time = timezone.now() + timedelta(days=1)  # Ensure start time is in the future
        with self.assertRaises(ValidationError) as context:
            Session.objects.create(
                title="Excessive Duration",
                description="Excessive combined durations",
                session_start_time=future_start_time,
                choice_duration=timedelta(days=10),
                voting_duration=timedelta(days=20),
            )
        self.assertIn("The combined duration of choice and voting exceeds the allowed limit.", str(context.exception))
        mock_send_initial.assert_not_called()
        mock_send_reminder.assert_not_called()


    def test_excessive_length_title_description(self, mock_send_initial, mock_send_reminder):
        with self.assertRaises(ValidationError) as context:
            Session.objects.create(
                title="T" * 300,  # Excessively long title
                description="D" * 1000,  # Excessively long description
                session_start_time=timezone.now(),
                choice_duration=timedelta(hours=2),
                voting_duration=timedelta(hours=2),
            )
        self.assertIn("Ensure this value has at most 200 characters", str(context.exception))
        mock_send_initial.assert_not_called()
        mock_send_reminder.assert_not_called()

    def test_missing_required_fields(self, mock_send_initial, mock_send_reminder):
        with self.assertRaises(ValidationError) as context:
            Session.objects.create(
                title="",
                description="",
                session_start_time=timezone.now(),
                choice_duration=timedelta(hours=2),
                voting_duration=timedelta(hours=2),
            )
        self.assertIn("This field cannot be blank.", str(context.exception))
        mock_send_initial.assert_not_called()
        mock_send_reminder.assert_not_called()

    def test_negative_duration(self, mock_send_initial, mock_send_reminder):
        with self.assertRaises(ValidationError) as context:
            Session.objects.create(
                title="Negative Duration",
                description="Duration cannot be negative",
                session_start_time=timezone.now(),
                choice_duration=timedelta(hours=-2),
                voting_duration=timedelta(hours=-3),
            )
        self.assertIn("Choice duration must be a positive value.", str(context.exception))
        mock_send_initial.assert_not_called()
        mock_send_reminder.assert_not_called()
