from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
from games.models import Game

# Create your models here.
DOWNLOAD_STATE = [
    ('Downloaded', 'Downloaded'),
    ('Not Downloaded', 'Not Downloaded'),
]

class Library(models.Model):
    account = models.ForeignKey(Profile, related_name='libraries', on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    download_state = models.CharField(choices=DOWNLOAD_STATE, max_length=15, default="Not Downloaded")
    
    # class Meta:
        # ordering = ['timestamp']
        # unique_together = ('account', 'game')  # Ensure unique combination
        
    def __str__(self):
        return f"{self.account} - {self.game}"