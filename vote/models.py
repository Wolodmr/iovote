from django.db import models
from voting_sessions.models import Session

class Vote(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='votes')
    user = models.CharField(max_length=100)
    option = models.CharField(max_length=100)


