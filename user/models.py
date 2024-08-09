from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    userName = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    avatar = models.ImageField(upload_to='user/avatars/')
    
    def __str__(self):
        return f"{self.userName.first_name} {self.userName.last_name}"