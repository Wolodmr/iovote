from django.db import models

class Result(models.Model):
    """Model to store voting session results."""
    
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        app_label = 'results'

    def __str__(self):
        """Return a string representation of the result."""
        return self.name

    


