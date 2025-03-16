# voting_sessions/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import get_user_model


def calculate_default_end_time():
    return timezone.now() + timezone.timedelta(days=3)

class Session(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, unique=True)
    session_start_time = models.DateTimeField(null=True, blank=True)
    session_end_time = models.DateTimeField(default=calculate_default_end_time, null=True, blank=True)
    choice_duration = models.DurationField(null=True, blank=True, default=timezone.timedelta(hours=1))
    voting_duration = models.DurationField(null=True, blank=True, default=timezone.timedelta(hours=1))
    description = models.TextField(default="Default description", null=True, blank=True)
    email_sent = models.BooleanField(default=False)
    creator_email = models.EmailField(max_length=255, blank=True, null=True, default="admin@example.com")
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    users = models.ManyToManyField(User, related_name="sessions")
    

    def get_invite_link(self):
        """Generate a direct invite link for this session."""
        from django.urls import reverse
        return reverse('voting_sessions:session_invite', args=[self.uuid])

    def __str__(self):
        return self.title
    
    def send_invites(self):
        """Send email invitations with the session invite link to all users."""
        invite_link = f"{settings.SITE_URL}{self.get_invite_link()}"  # Full URL
        subject = f"Invitation to Vote in: {self.title}"
        message = f"Dear Voter,\n\nYou are invited to participate in the voting session '{self.title}'.\n" \
                  f"Click the link below to access the session:\n\n{invite_link}\n\n" \
                  "Thank you for your participation!"
        
        # Fetch all registered users' emails
        User = get_user_model()
        recipient_list = list(User.objects.exclude(email="").values_list('email', flat=True))

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            self.email_sent = True
            self.save()

    @property
    def voting_start_time(self):
        return self.session_start_time + self.choice_duration

    @property
    def voting_end_time(self):
        return self.voting_start_time + self.voting_duration

    def is_active(self):
        print(f"DEBUG: session_end_time = {self.session_end_time}")  # Debugging output
        return self.session_end_time and self.session_end_time >= timezone.now()

    def is_voting_active(self):
        now = timezone.now()
        return self.voting_start_time <= now <= self.voting_end_time

    def send_notification(self):
        if self.creator_email:
            send_mail(
                subject=f'Notification for session: {self.title}',
                message=f'The session "{self.title}" has been created/updated.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.creator_email],
                fail_silently=False,
            )

    def clean(self):
        if self.session_start_time and timezone.is_naive(self.session_start_time):
            raise ValidationError("Session start time must be timezone-aware.")
        if self.session_end_time and timezone.is_naive(self.session_end_time):
            raise ValidationError("Session end time must be timezone-aware.")
        if self.session_start_time and self.session_start_time < timezone.now():
            raise ValidationError("Session start time cannot be in the past.")
        if self.session_end_time and self.session_start_time and self.session_end_time < self.session_start_time:
            raise ValidationError("Session end time must be after the start time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or self.has_changes():
            self.send_notification()

    def has_changes(self):
        if not self.pk:
            return False
        original = Session.objects.get(pk=self.pk)
        fields_to_check = ['title', 'description', 'session_start_time', 'choice_duration', 'voting_duration']
        for field in fields_to_check:
            if getattr(self, field) != getattr(original, field):
                return True
        return False
    
    def get_options(self):
            """Returns all options related to this session."""
            return self.options.all()  # ✅ Correct way to access options

class Option(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='options')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
