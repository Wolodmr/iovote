# voting_sessions/models.py
from django.db import models
from datetime import timedelta

class Session(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    session_start_time = models.DateTimeField()
    choice_duration = models.PositiveIntegerField()  # In days
    voting_duration = models.PositiveIntegerField()  # In days

    @property
    def session_end_time(self):
        return self.session_start_time + timedelta(
            days=self.choice_duration + self.voting_duration
        )

class Option(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="options")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
