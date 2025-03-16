#results/tests.py 

from django.test import TestCase
from datetime import timedelta
from django.urls import reverse
from voting_sessions.models import Session
from django.utils import timezone


class ResultsViewTest(TestCase):
    """Test case for results views."""

    def setUp(self):
        """Set up test data before each test."""
        self.session = Session.objects.create(
            title="Test Session",
            session_start_time=timezone.now() + timedelta(days=1),
            choice_duration=timedelta(minutes=5),
            voting_duration=timedelta(minutes=10),
            email_sent=False,
            description="A test session"
        )

    def test_results_list_view(self):
        """Test if the results list view returns a 200 status and contains session title."""
        response = self.client.get(reverse('results:results_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Session")

    def test_results_detail_view(self):
        """Test if the results detail view returns a 200 status and contains session title."""
        response = self.client.get(reverse('results:results_detail', args=[self.session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Session")
