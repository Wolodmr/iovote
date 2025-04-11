from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid


def calculate_default_end_time():
    return timezone.now() + timezone.timedelta(days=1)


class Session(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, unique=True)
    session_start_time = models.DateTimeField(null=True, blank=True, db_index=True)  # ✅ Indexed
    session_end_time = models.DateTimeField(default=calculate_default_end_time, null=True, blank=True, db_index=True)  
    choice_duration = models.DurationField(null=True, blank=True, default=timezone.timedelta(hours=1))
    voting_duration = models.DurationField(null=True, blank=True, default=timezone.timedelta(hours=1))
    description = models.TextField(default="Default description", null=True, blank=True)
    email_sent = models.BooleanField(default=False, db_index=True)  # ✅ Indexed
    creator_email = models.EmailField(max_length=255, blank=True, null=True, default="admin@example.com")
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    users = models.ManyToManyField(get_user_model(), related_name="sessions", through="SessionUser")  # ✅ Optimized ManyToMany

    class Meta:
        indexes = [
            models.Index(fields=["session_start_time"]),  # ✅ Index for fast querying
        ]

    def get_invite_link(self):
        """Generate a direct invite link for this session."""
        from django.urls import reverse
        return reverse("voting_sessions:session_invite", args=[self.uuid])

    def __str__(self):
        return self.title

    def send_invites(self):
        """Send email invitations to all users."""
        invite_link = f"{settings.SITE_URL}{self.get_invite_link()}"
        subject = f"Invitation to Vote in: {self.title}"
        message = (
            f"Dear Voter,\n\nYou are invited to participate in the voting session '{self.title}'.\n"
            f"Click the link below to access the session:\n\n{invite_link}\n\nThank you for your participation!"
        )

        # ✅ Optimized email fetching
        recipient_list = list(self.users.values_list("email", flat=True).filter(email__gt=""))

        if recipient_list:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipient_list,
                fail_silently=False,
            )
            self.email_sent = True
            self.save(update_fields=["email_sent"])  # ✅ Update only the changed field

    @property
    def voting_start_time(self):
        return self.session_start_time + self.choice_duration

    @property
    def voting_end_time(self):
        return self.voting_start_time + self.voting_duration

    def is_active(self):
        return self.session_end_time and self.session_end_time >= timezone.now()

    def is_voting_active(self):
        now = timezone.now()
        return self.voting_start_time <= now <= self.voting_end_time

    def send_notification(self):
        """Notify the creator about session updates."""
        if self.creator_email:
            send_mail(
                subject=f"Notification for session: {self.title}",
                message=f'The session "{self.title}" has been created/updated.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.creator_email],
                fail_silently=False,
            )

    def clean(self):
        """Ensure valid datetime constraints."""
        if self.session_start_time and timezone.is_naive(self.session_start_time):
            raise ValidationError("Session start time must be timezone-aware.")
        if self.session_end_time and timezone.is_naive(self.session_end_time):
            raise ValidationError("Session end time must be timezone-aware.")
        if self.session_start_time and self.session_start_time < timezone.now():
            raise ValidationError("Session start time cannot be in the past.")
        if self.session_end_time and self.session_start_time and self.session_end_time < self.session_start_time:
            raise ValidationError("Session end time must be after the start time.")

    def save(self, *args, **kwargs):
        """Optimize save method to prevent unnecessary saves."""
        is_new = self._state.adding  # ✅ More efficient than checking `self.pk`
        
        if is_new:
            super().save(*args, **kwargs)
            self.send_notification()
            return

        if self.has_changes():
            super().save(*args, **kwargs)
            self.send_notification()
        else:
            super().save(*args, update_fields=kwargs.get("update_fields", None))  # ✅ Avoid full update if not needed

    def has_changes(self):
        """Check if tracked fields have changed before saving."""
        if self._state.adding:  # ✅ If it's a new instance, return False
            return False
        
        fields_to_check = ["title", "description", "session_start_time", "choice_duration", "voting_duration"]
        original = Session.objects.filter(pk=self.pk).only(*fields_to_check).first()  # ✅ Efficient field selection

        if not original:
            return False  # If session doesn't exist in DB, it's a new instance

        return any(getattr(self, field) != getattr(original, field) for field in fields_to_check)

    def get_options(self):
        """Returns all options related to this session."""
        return self.options.select_related("session").all()  # ✅ Avoids extra queries


class Option(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="options")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title


class SessionUser(models.Model):  # ✅ Custom ManyToMany Table (More Efficient)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ("session", "user")  # ✅ Prevent duplicate entries
