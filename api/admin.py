from django.contrib import admin
from .models import Community
from .models import Message
from .models import JournalEntry
from .models import UserSettings
from .models import Todo
from .models import MoodAssessment
from .models import BotSettings
from .models import UserConversation

# Register your models here

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications', 'sms_notifications', 'profile_visibility', 'search_visibility', 'current_theme']
    list_filter = ['email_notifications', 'push_notifications', 'sms_notifications', 'profile_visibility', 'search_visibility', 'current_theme']
    search_fields = ['user__username', 'user__email']  # Assuming 'user' is the foreign key to the User model

class MessageAdmin(admin.ModelAdmin):
    list_display = ('community', 'content', 'user', 'timestamp')
    list_display_links = ('content',) 

# Register the Message model with the MessageAdmin class
admin.site.register(Message, MessageAdmin)


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')

@admin.register(JournalEntry)
class JournalEntry(admin.ModelAdmin):
    list_display = ('title', 'content', 'timestamp','user','background_color')

class TodoAdmin(admin.ModelAdmin):
    # Define fields to display in the admin panel
    list_display = ('id', 'text', 'deadline','user')
    
@admin.register(MoodAssessment)
class MoodAssessment (admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'happiness','anxiety', 'energy', 'sleep_quality', 'appetite', 'physical_health', 'concentration', 'social_connections', 'stress_level')

# Register the Todo model with the custom admin options
admin.site.register(Todo, TodoAdmin)

@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bot_name', 'created_at', 'updated_at')
    search_fields = ('user__username', 'bot_name')
    list_filter = ('created_at', 'updated_at')
    ordering = ('-updated_at',)

@admin.register(UserConversation)
class UserConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'bot_response', 'timestamp')
    search_fields = ('user__username', 'user_message')  # Search by username
    list_filter = ('timestamp',)
    ordering = ['-timestamp']