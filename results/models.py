from django.db import models

class Result(models.Model):
    # Define fields for the Result model
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    class Meta:
        app_label = 'results'

    


