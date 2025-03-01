# voting_sessions/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.timezone import timedelta, make_aware
from django.utils import timezone
from django.utils.timezone import now
from django.utils.timezone import localtime
from django.utils import timezone    
from django.core.exceptions import ValidationError

def calculate_default_end_time():
        return timezone.now() + timedelta(days=3)
    
class Session(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)  # Single title for the session (choices + voting)
    session_start_time = models.DateTimeField(null=True, blank=True)  # When the session starts (choices phase)
    session_end_time = models.DateTimeField(default=calculate_default_end_time, null=True, blank=True)
    choice_duration = models.DurationField(null=True, blank=True, default=timedelta(hours=1))  # Duration of the choices phase
    voting_duration = models.DurationField(null=True, blank=True, default=timedelta(hours=1))  # Duration of the voting phase
    description = models.TextField(default="Default description", null=True, blank=True)  # Session description
    email_sent = models.BooleanField(default=False)
    creator_email = models.EmailField(max_length=255, blank=True, null=True, default="postvezha@gmail.com")
    invitation_endpoint = models.URLField(max_length=500, blank=True, null=True, default="https://example.comm")

    def __str__(self):
        return self.title    
    
    @property
    def voting_start_time(self):
        return self.session_start_time + self.choice_duration

    @property
    def voting_end_time(self):
        return self.voting_start_time + self.voting_duration

    def is_active(self):
        now = timezone.now()
        return self.session_start_time <= now <= self.session_end_time

    def is_voting_active(self):
        now = timezone.now()
        return self.voting_start_time <= now <= self.voting_end_time
    
    def send_notification(self):
        """
        Send notifications for the session via email 
        """
        # Email logic (placeholder for now)
        print(f"Email notification sent for session: {self}")

    def clean(self):
        
        # Ensure datetime fields are aware before validation
        if timezone.is_naive(self.session_start_time):
            raise ValidationError("Session start time must be timezone-aware.")
        if timezone.is_naive(self.session_end_time):
            raise ValidationError("Session end time must be timezone-aware.")

        # Validate start and end times
        if localtime(self.session_start_time) < timezone.now():
            raise ValidationError("Session start time cannot be in the past.")
        if localtime(self.session_end_time) < self.session_start_time:
            raise ValidationError("Session end time must be after the start time.")

        
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

    
class Option(models.Model):
    session = models.ForeignKey('voting_sessions.Session', on_delete=models.CASCADE, related_name='options')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
    
# In your models.py
class Meta:
    app_label = 'voting_sessions'


