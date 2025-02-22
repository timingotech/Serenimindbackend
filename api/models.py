from django.db import models
import uuid
from django.contrib.auth.models import User
from django.contrib import admin
from django.conf import settings

class UserSettings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    profile_visibility = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    search_visibility = models.CharField(max_length=10, choices=[('public', 'Public'), ('private', 'Private')], default='public')
    current_theme = models.CharField(max_length=10, choices=[('light', 'Light'), ('dark', 'Dark')], default='light')

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
    
class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    fullname = models.CharField(max_length=255)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    background_color = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return self.title

class CommunityPost(models.Model):
    content = models.TextField()
    user_id = models.IntegerField()
    username = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.username} at {self.timestamp}"
    
class Community(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    community = models.ForeignKey(Community, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    list_display = ('community', 'content', 'user', 'timestamp')
    list_display_links = ('content',) 

    def __str__(self):
        return self.content
    
class Report(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    
class Todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    deadline = models.DateField()
    completed = models.BooleanField(default=False)

class MoodEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()
    mood_rating = models.IntegerField()
    notes = models.TextField(blank=True)


class MoodAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    happiness = models.IntegerField()
    anxiety = models.CharField(max_length=20)
    energy = models.CharField(max_length=20)
    sleep_quality = models.IntegerField()
    appetite = models.IntegerField()
    physical_health = models.IntegerField()
    concentration = models.IntegerField()
    social_connections = models.IntegerField()
    stress_level = models.IntegerField()

    def __str__(self):
        return f"{self.user.username}'s mood assessment on {self.timestamp}"

class ChatHistory(models.Model):
    session_id = models.CharField(max_length=255)
    message = models.TextField()
    intent = models.CharField(max_length=255)
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class BotSettings(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bot_settings'
    )
    bot_name = models.CharField(max_length=50, default='SereniAI')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user']

class UserConversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations", null=True)  # Make it nullable temporarily
    user_message = models.TextField()
    bot_response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation with {self.user.username if self.user else 'Unknown'} at {self.timestamp}"
