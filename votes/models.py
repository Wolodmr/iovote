from django.db import models
from django.contrib.auth.models import User

class VotingOption(models.Model):
    name = models.CharField(max_length=255)
    session = models.ForeignKey('VotingSession', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class VotingSession(models.Model):
    name = models.CharField(max_length=200)
    start_time = models.TimeField()
    end_time = models.TimeField()
    start_date = models.DateField()
    end_date = models.DateField()
    participant_count = models.PositiveIntegerField(default=0)
   
    def __str__(self):
        return f"{self.name} ({self.start_date} to {self.end_date})"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(VotingOption, on_delete=models.CASCADE, null=True, blank=True)  # Option can be None for "no support" votes
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, null=True)
    no_support = models.BooleanField(default=False)

    def __str__(self):
        return f"Vote for {self.option.name}"




class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Participation(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE)
    voted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.reader.name} in session {self.session.name}"


    





