from django.db import models

class Result(models.Model):
    """Model to store voting session results."""
    
    option = models.CharField(max_length=100)
    votes = models.IntegerField(default=0)  # ✅ Ensure this field exists

    def __str__(self):
        return f"{self.option} - {self.votes} votes"

    


