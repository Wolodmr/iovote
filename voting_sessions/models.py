from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.timezone import timedelta
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

def calculate_default_end_time():
    """Default session end time: 3 days from now"""
    return timezone.now() + timedelta(days=3)

class Session(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True)
    session_start_time = models.DateTimeField(null=True, blank=True)
    session_end_time = models.DateTimeField(default=calculate_default_end_time, null=True, blank=True)
    choice_duration = models.DurationField(null=True, blank=True, default=timedelta(hours=1))
    voting_duration = models.DurationField(null=True, blank=True, default=timedelta(hours=1))
    description = models.TextField(default="Default description", null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    
    # Automatically set to admin email from settings
    creator_email = models.EmailField(
        max_length=255, 
        blank=True, 
        null=True, 
        default=settings.ADMIN_EMAIL  
    )

    # Auto-generated invitation link
    invitation_endpoint = models.URLField(
        max_length=500, 
        blank=True, 
        null=True, 
        editable=False  
    )

    def __str__(self):
        return self.title or "Unnamed Session"
    
    @property
    def voting_start_time(self):
        if self.session_start_time and self.choice_duration:
            return self.session_start_time + self.choice_duration
        return None

    @property
    def voting_end_time(self):
        if self.voting_start_time and self.voting_duration:
            return self.voting_start_time + self.voting_duration
        return None

    def is_active(self):
        """Check if the session is currently active"""
        now = timezone.localtime()
        return self.session_start_time and self.session_start_time <= now <= self.session_end_time

    def is_voting_active(self):
        """Check if voting is currently active"""
        now = timezone.localtime()
        return self.voting_start_time and self.voting_start_time <= now <= self.voting_end_time

    def get_invitation_link(self):
        """Generate the session detail page link dynamically"""
        site_url = getattr(settings, "SITE_URL", "http://127.0.0.1:8000")  
        return f"{site_url}{reverse('session_detail', args=[self.id])}"

    def send_notification(self):
        """Send email notification when a session is created or updated"""
        if self.creator_email:
            send_mail(
                subject=f"Session Notification: {self.title}",
                message=f"A new session has been created: {self.title}.\nDescription: {self.description}",
                from_email="noreply@example.com",
                recipient_list=[self.creator_email],
                fail_silently=True,
            )

    def clean(self):
        """Ensure valid session timings"""
        if self.session_start_time and timezone.is_naive(self.session_start_time):
            raise ValidationError("Session start time must be timezone-aware.")
        if self.session_end_time and timezone.is_naive(self.session_end_time):
            raise ValidationError("Session end time must be timezone-aware.")

        if self.session_start_time and self.session_start_time < timezone.now():
            raise ValidationError("Session start time cannot be in the past.")
        if self.session_end_time and self.session_end_time < self.session_start_time:
            raise ValidationError("Session end time must be after the start time.")

    def save(self, *args, **kwargs):
        """Save session with validation and notification"""
        self.full_clean()

        # Auto-generate the invitation link
        if not self.invitation_endpoint:
            self.invitation_endpoint = self.get_invitation_link()
        
        is_new = self.pk is None  
        super().save(*args, **kwargs)
        
        if is_new or self.has_changes():
            self.send_notification()

    def has_changes(self):
        """Check if key fields have changed"""
        original = type(self).objects.filter(pk=self.pk).first()
        if not original:
            return False
        fields_to_check = ["title", "description", "session_start_time", "choice_duration", "voting_duration"]
        return any(getattr(self, field) != getattr(original, field) for field in fields_to_check)

class Option(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='options')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
