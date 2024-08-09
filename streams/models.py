from django.db import models
from django.contrib.auth.models import User
from user.models import Profile
from games.models import Game

# Create your models here.
class Stream(models.Model):
    title = models.CharField(max_length=100)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='streams/images/')
    streamer = models.ForeignKey(Profile, on_delete=models.CASCADE)
    url = models.URLField()
    
    def __str__(self):
        return f"{self.game} - {self.streamer}"