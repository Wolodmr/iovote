# voting_sessions/models.py

from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.mail import send_mail, get_connection
from django.utils.html import strip_tags
from django.utils.timezone import localtime
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
import logging
import uuid

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename="email_debug.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def calculate_default_end_time():
    return timezone.now() + timezone.timedelta(days=1)

class Session(models.Model):
    title = models.CharField(max_length=200, null=True, blank=True, unique=True)
    session_start_time = models.DateTimeField(null=True, blank=True, db_index=True)
    session_end_time = models.DateTimeField(default=calculate_default_end_time, null=True, blank=True, db_index=True)
    choice_duration = models.DurationField(default=timezone.timedelta(minutes=1), null=True, blank=True)
    voting_duration = models.DurationField(default=timezone.timedelta(hours=1), null=True, blank=True)
    description = models.TextField(default="Default description", null=True, blank=True)
    email_sent = models.BooleanField(default=False, db_index=True)
    creator_email = models.EmailField(max_length=255, default="postvezha@gmail.com", null=True, blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    users = models.ManyToManyField(get_user_model(), related_name="sessions", through="SessionUser")

    class Meta:
        indexes = [models.Index(fields=["session_start_time"])]

    def __str__(self):
        return self.title or "Untitled Session"

    def get_invite_link(self):
        return reverse("voting_sessions:session_invite", args=[self.uuid])

    def get_invite_url(self):
        return f"{settings.SITE_URL}{self.get_invite_link()}"

    def get_recipient_emails(self):
        return list(self.users.filter(email__gt="").values_list("email", flat=True))

    def send_invites(self):
        """Send invite emails to all assigned users."""
        recipient_list = self.get_recipient_emails()
        if not recipient_list:
            logger.info(f"No invite emails sent for session '{self.title}': no recipients.")
            return

        send_mail(
            subject=f"Invitation to Vote in: {self.title}",
            message=(
                f"Dear Voter,\n\n"
                f"You are invited to participate in the voting session '{self.title}'.\n"
                f"Access the session here: {self.get_invite_url()}\n\n"
                f"Thank you for your participation!"
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=recipient_list,
            fail_silently=False,
        )
        self.email_sent = True
        self.save(update_fields=["email_sent"])
        logger.info(f"Invites sent for session '{self.title}'.")

    def send_notification(self):
        """Notify all users with emails about session creation/update."""
        User = get_user_model()
        recipient_list = list(User.objects.filter(email__gt="").values_list("email", flat=True))
        if not recipient_list:
            logger.warning(f"No valid recipients for session notification: {self.title}")
            return

        start_time = localtime(self.session_start_time).strftime('%Y-%m-%d %H:%M %Z')
        end_time = localtime(self.session_end_time).strftime('%Y-%m-%d %H:%M %Z')
        voting_start = self.voting_start_time
        voting_start_disp = localtime(voting_start).strftime('%Y-%m-%d %H:%M %Z')

        # Format choice duration nicely
        duration = self.choice_duration
        seconds = duration.total_seconds()
        if seconds < 3600:
            choice_disp = f"{int(seconds // 60)} minutes"
        elif seconds < 86400:
            choice_disp = f"{int(seconds // 3600)} hours"
        else:
            choice_disp = f"{int(duration.days)} days"

        voting_url = "https://vote-cast.onrender.com/"

        subject = f"🚀 Ready to Vote? A New Session '{self.title}' Awaits You!"
        html_message = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6;">
            <h2 style="color: #2e6c80;">🗳️ New Session: {self.title}</h2>
            <p><strong>Description:</strong><br>{self.description}</p>
            <p><strong>🗓️ Start Time:</strong> {start_time}</p>
            <p><strong>⏳ Choice Duration:</strong> {choice_disp}</p>
            <p style="margin-left: 1.5em; font-style: italic;">
                This time is suggested for reflection, discussion, or research.
            </p>
            <p><span style="color: green;"><strong>🗓️ Voting Starts:</strong> {voting_start_disp}</span></p>
            <p><strong>⏱️ End Time:</strong> {end_time}</p>
            <p style="margin-top: 30px; font-weight: bold; font-size: 1.2em; color: #1a3f2b;">Ready to Vote?</p>
            <p><a href="{voting_url}" style="padding:10px 15px; background:#527930; color:white; text-decoration:none; border-radius:5px;">Cast Your Vote</a></p>
        </body>
        </html>
        """
        plain_message = strip_tags(html_message)

        try:
            with get_connection(backend=settings.EMAIL_BACKEND) as connection:
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=recipient_list,
                    html_message=html_message,
                    connection=connection,
                    fail_silently=False,
                )
            logger.info(f"Notification email sent successfully for session: {self.title}")
        except Exception as e:
            logger.error(f"Error sending session notification '{self.title}': {e}", exc_info=True)

    def clean(self):
        if self.session_start_time and timezone.is_naive(self.session_start_time):
            raise ValidationError("Session start time must be timezone-aware.")
        if self.session_end_time and timezone.is_naive(self.session_end_time):
            raise ValidationError("Session end time must be timezone-aware.")
        if self.session_start_time and self.session_start_time < timezone.now():
            raise ValidationError("Session start time cannot be in the past.")
        if self.session_end_time and self.session_start_time and self.session_end_time < self.session_start_time:
            raise ValidationError("Session end time must be after start time.")

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if is_new:
            super().save(*args, **kwargs)
            self.send_notification()
        elif self.has_changes():
            super().save(*args, **kwargs)
            self.send_notification()
        else:
            super().save(*args, update_fields=kwargs.get("update_fields", None))

    def has_changes(self):
        if self._state.adding:
            return False
        fields = ["title", "description", "session_start_time", "choice_duration", "voting_duration"]
        original = Session.objects.filter(pk=self.pk).only(*fields).first()
        return original and any(getattr(self, f) != getattr(original, f) for f in fields)

    def get_options(self):
        return self.options.select_related("session").all()

    @property
    def voting_start_time(self):
        return self.session_start_time + self.choice_duration

    @property
    def voting_end_time(self):
        return self.voting_start_time

    def is_active(self):
        return self.session_end_time and self.session_end_time >= timezone.now()

    def is_voting_active(self):
        now = timezone.now()
        return self.voting_start_time <= now <= self.voting_end_time

class Option(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="options")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class SessionUser(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = ("session", "user")
