# vote/models.py 

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from voting_sessions.models import Session
from django.utils.timezone import now

def default_session():
    return Session.objects.create(session_end_time=now()).id

class Vote(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    option = models.ForeignKey("voting_sessions.Option", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
   
    class Meta:
        app_label = 'vote'

    def __str__(self):
        return f'{self.user.username} voted for {self.option.title}'

def save(self, *args, **kwargs):
    if not self.option.session:
        raise ValidationError("This option is not linked to any session!")

    print(f"Assigning session: {self.option.session}")  # Debugging print
    self.session = self.option.session  # Ensure session is assigned

    if Vote.objects.filter(user=self.user, option__session=self.session).exists():
        raise ValidationError("You have already voted in this session.")

    super().save(*args, **kwargs)
def save(self, *args, **kwargs):
    if not self.option.session:
        raise ValidationError("This option is not linked to any session!")

    print(f"Assigning session: {self.option.session}")  # Debugging print
    self.session = self.option.session  # Ensure session is assigned

    print(f"Session ID in test: {self.session.id}")  # Add this here for debugging

    if Vote.objects.filter(user=self.user, option__session=self.session).exists():
        raise ValidationError("You have already voted in this session.")

    super().save(*args, **kwargs)


        
    
    
    
