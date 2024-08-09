from django.db import models

# Create your models here.
class Game(models.Model):
    title = models.CharField(max_length=100)
    owner = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='games/images/')
    thumbnail = models.ImageField(upload_to='games/thumbnails/')
    video = models.URLField(max_length=300)
    rating = models.FloatField()
    download_count = models.FloatField()
    size = models.IntegerField()
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    SS1 = models.ImageField(upload_to='games/screenshots/')
    SS2 = models.ImageField(upload_to='games/screenshots/')
    SS3 = models.ImageField(upload_to='games/screenshots/')
    download_link = models.URLField(max_length=300)
    
    def __str__(self):
        return f"{self.title} - {self.genre}"