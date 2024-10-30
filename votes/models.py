from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class VotingOption(models.Model):
    name = models.CharField(max_length=255)
    session = models.ForeignKey('VotingSession', on_delete=models.CASCADE)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class VotingSession(models.Model): 
    VOTING_DURATION_CHOICES = [
        (15, '15 days'),
        (30, '30 days'),
    ]
    name = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    duration = models.IntegerField(choices=VOTING_DURATION_CHOICES, default=30)
    voting_preference = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')], default='closed')
    is_started = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    def display_voting_options(self):
        # Fetch related VotingOption objects
        options = self.votingoption_set.all()  # or use related_name if defined
        # Format as a comma-separated string, or adjust as needed
        return ", ".join([option.name for option in options])

    display_voting_options.short_description = "Voting Options"  # Label for the admin panel

    def preliminary_voting_ends(self):
        end_time = None
        if self.duration == 30:
            end_time = self.start_date + timezone.timedelta(days=19)
        elif self.duration == 15:
            end_time = self.start_date + timezone.timedelta(days=9)
        
        print(f"[DEBUG] Preliminary voting ends at: {end_time}")  # Debugging output
        return end_time

    def votes_per_option(self):
        return {
            option.name: Vote.objects.filter(option=option, session=self).count()
            for option in self.votingoption_set.all()
        }

    def __str__(self):
        return self.name

# In models.py
from django.db.models import Count

class PreliminaryVoting(models.Model):
    # Model fields
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE, related_name="preliminary_votings")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    preference = models.CharField(max_length=10, choices=[('open', 'Open'), ('closed', 'Closed')])
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.preference} ({self.session})"

    @classmethod
    def open_votes_count(cls, session_id):
        return cls.objects.filter(session_id=session_id, preference='open').count()

    @classmethod
    def closed_votes_count(cls, session_id):
        return cls.objects.filter(session_id=session_id, preference='closed').count()


    def preliminary_votes_count(self):
        end_preliminary_date = self.session.preliminary_voting_ends()
        print(f"[DEBUG] Counting preliminary votes before: {end_preliminary_date}")

        # Counting only votes within the preliminary voting period
        votes_count = Vote.objects.filter(session=self.session, timestamp__lt=end_preliminary_date).count()
        print(f"[DEBUG] Total preliminary votes count: {votes_count}")
        
        return votes_count

    def open_votes_percentage(self):
        total = self.preliminary_votes_count()
        if total == 0:
            return 0
        percentage = round((self.open_votes_count() / total) * 100, 1)
        print(f"[DEBUG] Open votes percentage: {percentage}")  # Debugging output
        return percentage


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    option = models.ForeignKey(VotingOption, on_delete=models.SET_NULL, null=True, blank=True)  # Allow "no support" votes
    session = models.ForeignKey(VotingSession, on_delete=models.CASCADE)  # Consider removing null=True if not needed
    no_support = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.option.name if self.option else "No Option"



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





 
    


    





