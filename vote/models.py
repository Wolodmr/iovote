# vote/models.py 

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from voting_sessions.models import Session
from django.utils.timezone import now

def default_session():
    return Session.objects.create(session_end_time=now()).id

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    option = models.ForeignKey("voting_sessions.Option", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.ForeignKey('voting_sessions.Session', on_delete=models.CASCADE, null=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'option'], name='unique_user_option_vote'),
        ]

    def __str__(self):
        return f'{self.user.username} voted for {self.option.title}'

    # def clean(self):
    #     # Check if the user has already voted in the session of the selected option
    #     if Vote.objects.filter(user=self.user, option__session=self.option.session).exists():
    #         raise ValidationError("You have already voted in this session.")

    def save(self, *args, **kwargs):
            # Call the clean method to enforce the validation before saving
            self.clean()
            super().save(*args, **kwargs)
    # def save(self, *args, **kwargs):
    #     if not self.option.session:
    #         raise ValidationError("This option is not linked to any session!")

    #     print(f"Assigning session: {self.option.session}")  # Debugging print
    #     self.session = self.option.session  # Ensure session is assigned

    #     print(f"Session ID in test: {self.session.id}")  # Add this here for debugging

    #     if Vote.objects.filter(user=self.user, option__session=self.session).exists():
    #         raise ValidationError("You have already voted in this session.")

    #     super().save(*args, **kwargs)


        
    
    
    
