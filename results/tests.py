#results/tests.py 

from django.test import TestCase
from datetime import timedelta, datetime
from django.urls import reverse
from voting_sessions.models import Session  # Replace with your actual session model
from django.utils import timezone
from django.conf import settings

print("DEBUG FINAL EMAIL_BACKEND:", settings.EMAIL_BACKEND)
print("DEBUG FINAL EMAIL_HOST:", settings.EMAIL_HOST)
print("DEBUG FINAL EMAIL_PORT:", settings.EMAIL_PORT)
print("DEBUG FINAL EMAIL_HOST_USER:", settings.EMAIL_HOST_USER)
print("DEBUG FINAL EMAIL_HOST_PASSWORD:", settings.EMAIL_HOST_PASSWORD)


class ResultsViewTest(TestCase):
    def setUp(self):
        self.session = Session.objects.create(title="Test Session")
    
    def setUp(self):
        self.session = Session.objects.create(
        title="Test Session",
        session_start_time=timezone.now() + timedelta(days=1),
        choice_duration=timedelta(minutes=5),
        voting_duration=timedelta(minutes=10),
        email_sent = False,
        description="A test session"
    )

    def test_results_list_view(self):
        response = self.client.get(reverse('results:results_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Session")

    def test_results_detail_view(self):
        response = self.client.get(reverse('results:results_detail', args=[self.session.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Session")
