# vote/models.py 

from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from voting_sessions.models import Session
from django.utils.timezone import now


class Vote(models.Model):
    """
    Model representing a user's vote for a specific option in a session.

    Attributes:
        user (User): The user who cast the vote.
        option (Option): The option that was voted for.
        created_at (datetime): The timestamp when the vote was created.
        session (Session): The voting session associated with the vote.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    option = models.ForeignKey("voting_sessions.Option", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    session = models.ForeignKey('voting_sessions.Session', on_delete=models.CASCADE, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'option'], name='unique_user_option_vote'),
        ]

    def __str__(self):
        """Return a string representation of the vote."""
        return f'{self.user.username} voted for {self.option.title}'

    def save(self, *args, **kwargs):
        """
        Override save method to enforce validation before saving.

        Raises:
            ValidationError: If the user has already voted in the session.
        """
        self.clean()
        super().save(*args, **kwargs)


        
    
    
    
