# voting_sessions/models.py
from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from .utils import broadcast_message_to_chat

class Session(models.Model):
    title = models.CharField(max_length=200)
    session_start_time = models.DateTimeField()
    choice_duration = models.DurationField()
    voting_duration = models.DurationField()
    description = models.TextField()
    creator_email = models.EmailField(max_length=255, blank=True, null=True, default="default@example.com")
    invitation_endpoint = models.URLField(max_length=500, blank=True, null=True, default="http://example.com/invite")


    def __str__(self):
        return self.title
    
    def send_notification(self):
        """
        Send notifications for the session via email and internal chat.
        """
        # Email logic (placeholder for now)
        print(f"Email notification sent for session: {self}")

        # Internal chat notification logic
        chat_message = (
            f"New session created: {self.title}\n"
            f"Start Time: {self.session_start_time}\n"
            f"Description: {self.description}\n"
            f"Participate here: {self.invitation_endpoint}"
        )
        
        try:
            broadcast_message_to_chat(chat_message)
            print(f"Chat notification sent for session: {self}")
        except Exception as e:
            print(f"Failed to send chat notification for session {self}: {e}")
    
    def clean(self):
    # Validate that choice_duration and voting_duration are not None
        if self.choice_duration is None:
            raise ValidationError("Choice duration cannot be null.")
        if self.voting_duration is None:
            raise ValidationError("Voting duration cannot be null.")
        
        # Validate durations are positive
        if self.choice_duration <= timedelta(0):
            raise ValidationError("Choice duration must be a positive value.")
        if self.voting_duration <= timedelta(0):
            raise ValidationError("Voting duration must be a positive value.")

        # Validate start time is not in the past
        if self.session_start_time < timezone.now():
            raise ValidationError("Session start time cannot be in the past.")
        max_duration = timedelta(days=24)
        if self.choice_duration + self.voting_duration > max_duration:
            raise ValidationError("The combined duration of choice and voting exceeds the allowed limit.")

        
    def save(self, *args, **kwargs):
        self.full_clean()  # Ensure validations are applied
        is_new = self.pk is None  # Check if the instance is being created for the first time
        super().save(*args, **kwargs)
        
        # Call send_notification only if the instance is newly created or updated
        if is_new or self.has_changes():
            self.send_notification()

    def has_changes(self):
        """
        Check if certain fields have changed before calling `send_notification`.
        """
        original = type(self).objects.filter(pk=self.pk).first()
        if not original:
            return False
        # print(f"Original: {original.title}, New: {self.title}")  # Add print statement to debug
        return (
            self.title != original.title
            or self.description != original.description
            or self.session_start_time != original.session_start_time
            or self.choice_duration != original.choice_duration
            or self.voting_duration != original.voting_duration
        )

    
    @property
    def session_end_time(self):
        return self.session_start_time + self.choice_duration + self.voting_duration

class Option(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="options")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
