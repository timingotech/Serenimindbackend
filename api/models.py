from django.db import models
import uuid
from django.contrib.auth.models import User

class UserProfile(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    whyHere = models.TextField()
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.username
    
    verification_token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)

class Post(models.Model):
    user = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.timestamp}"