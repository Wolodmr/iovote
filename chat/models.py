# chat/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Message(models.Model):
    username = models.CharField(max_length=100)  # Username field
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)  # Timestamp field

    def __str__(self):
        return f"{self.username}: {self.content} [{self.timestamp}]"
    
class Room(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


