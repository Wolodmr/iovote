# vote/tests.py 

from django.test import TestCase
from django.utils import timezone
from voting_sessions.models import Session
from django.core.exceptions import ValidationError
from django.utils.timezone import make_aware
from datetime import timedelta
from django.urls import reverse
from unittest.mock import patch
from django.contrib.auth.models import User
from vote.models import Vote
from voting_sessions.models import Option, Session  # Replace with actual paths to models

class VoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser")
        start = timezone.now() + timedelta(days=1)
        self.session = Session.objects.create(
            title="Test Session",
            session_start_time=start,
            session_end_time=start + timedelta(days=3),  # Set a valid end time
            choice_duration=timedelta(minutes=5),
            voting_duration=timedelta(minutes=10),
            description="Test session description"
        )
        self.option = Option.objects.create(
            title="Test Option",
            session=self.session
        )
        self.vote = Vote.objects.create(user=self.user, option=self.option)

    def clean(self):
        if self.session_start_time and not self.session_start_time.tzinfo:
            self.session_start_time = make_aware(self.session_start_time)
        print('sst = ', self.session_start_time)
        if self.session_start_time < timezone.now():
            raise ValidationError("Session start time cannot be in the past.")

    def test_vote_creation(self):
        # Check that the vote's user and option match expectations
        self.assertEqual(self.vote.user, self.user)
        self.assertEqual(self.vote.option, self.option)
        self.assertTrue(isinstance(self.vote, Vote))
        self.assertEqual(str(self.vote), f"{self.user.username} voted for {self.option.title}")

class VoteViewTest(TestCase):
    def setUp(self):
        self.session = Session.objects.create(
            session_end_time=timezone.now()+timedelta(days=3),
            session_start_time=timezone.now() + timedelta(days=1),
            title= 'Test Option'
        )
        
    def test_vote_list_view(self):
        response = self.client.get(reverse('vote:vote', kwargs={'session_id': self.session.id}))  # Update 'vote_list' with actual URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'vote/vote.html')  # Update template name if needed



