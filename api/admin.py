from django.contrib import admin
from .models import Community
from .models import Message
from .models import JournalEntry
from .models import UserSettings
from .models import Todo
from .models import MoodAssessment
from .models import BotSettings
from .models import UserConversation
from django.utils.html import format_html

# Register your models here

@admin.register(UserSettings)
class UserSettingsAdmin(admin.ModelAdmin):
    list_display = ['user', 'email_notifications', 'push_notifications', 'sms_notifications', 'profile_visibility', 'search_visibility', 'current_theme']
    list_filter = ['email_notifications', 'push_notifications', 'sms_notifications', 'profile_visibility', 'search_visibility', 'current_theme']
    search_fields = ['user__username', 'user__email']
    list_per_page = 25
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Notification Settings', {
            'fields': ('email_notifications', 'push_notifications', 'sms_notifications')
        }),
        ('Privacy Settings', {
            'fields': ('profile_visibility', 'search_visibility')
        }),
        ('Appearance', {
            'fields': ('current_theme',)
        }),
    )

class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    fields = ('user', 'content', 'timestamp')
    readonly_fields = ('timestamp',)

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'message_count')
    search_fields = ['name', 'description']
    inlines = [MessageInline]
    list_per_page = 25
    
    def message_count(self, obj):
        count = obj.message_set.count()
        return format_html('<span style="color: #5b80b2; font-weight: bold;">{}</span>', count)
    message_count.short_description = 'Messages'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('community', 'user', 'short_content', 'timestamp', 'colored_user')
    list_filter = ['community', 'timestamp']
    search_fields = ['content', 'user__username', 'community__name']
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    list_per_page = 25
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    short_content.short_description = 'Content'
    
    def colored_user(self, obj):
        return format_html('<span style="color: #28a745; font-weight: bold;">{}</span>', obj.user.username)
    colored_user.short_description = 'User'

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'short_content', 'timestamp', 'color_badge')
    list_filter = ['timestamp', 'user']
    search_fields = ['title', 'content', 'user__username']
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    list_per_page = 25
    fieldsets = (
        ('Entry Information', {
            'fields': ('user', 'title', 'content')
        }),
        ('Styling', {
            'fields': ('background_color',)
        }),
        ('Metadata', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
    )
    
    def short_content(self, obj):
        return obj.content[:75] + '...' if len(obj.content) > 75 else obj.content
    short_content.short_description = 'Content'
    
    def color_badge(self, obj):
        return format_html(
            '<div style="width: 30px; height: 30px; background-color: {}; border-radius: 50%; border: 2px solid #ddd;"></div>',
            obj.background_color
        )
    color_badge.short_description = 'Color'

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'user', 'deadline', 'completed', 'status_badge')
    list_filter = ['completed', 'deadline', 'user']
    search_fields = ['text', 'user__username']
    date_hierarchy = 'deadline'
    list_per_page = 25
    actions = ['mark_completed', 'mark_incomplete']
    
    def status_badge(self, obj):
        if obj.completed:
            return format_html('<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">✓ Done</span>')
        else:
            return format_html('<span style="background-color: #ffc107; color: black; padding: 3px 10px; border-radius: 3px;">⏳ Pending</span>')
    status_badge.short_description = 'Status'
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated} task(s) marked as completed.')
    mark_completed.short_description = 'Mark selected as completed'
    
    def mark_incomplete(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated} task(s) marked as incomplete.')
    mark_incomplete.short_description = 'Mark selected as incomplete'
    
@admin.register(MoodAssessment)
class MoodAssessmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'timestamp', 'happiness_badge', 'anxiety', 'energy', 'stress_badge', 'sleep_quality')
    list_filter = ['timestamp', 'anxiety', 'energy']
    search_fields = ['user__username']
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    list_per_page = 25
    fieldsets = (
        ('User & Timestamp', {
            'fields': ('user', 'timestamp')
        }),
        ('Mental Health Indicators', {
            'fields': ('happiness', 'anxiety', 'stress_level', 'concentration')
        }),
        ('Physical Health', {
            'fields': ('energy', 'sleep_quality', 'appetite', 'physical_health')
        }),
        ('Social', {
            'fields': ('social_connections',)
        }),
    )
    
    def happiness_badge(self, obj):
        color = '#28a745' if obj.happiness > 7 else '#ffc107' if obj.happiness > 4 else '#dc3545'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}/10</span>',
            color, obj.happiness
        )
    happiness_badge.short_description = 'Happiness'
    
    def stress_badge(self, obj):
        color = '#dc3545' if obj.stress_level > 7 else '#ffc107' if obj.stress_level > 4 else '#28a745'
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}/10</span>',
            color, obj.stress_level
        )
    stress_badge.short_description = 'Stress'

@admin.register(BotSettings)
class BotSettingsAdmin(admin.ModelAdmin):
    list_display = ('user', 'bot_name', 'created_at', 'updated_at')
    search_fields = ('user__username', 'bot_name')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-updated_at',)
    list_per_page = 25

@admin.register(UserConversation)
class UserConversationAdmin(admin.ModelAdmin):
    list_display = ('user', 'short_user_message', 'short_bot_response', 'timestamp')
    search_fields = ('user__username', 'user_message', 'bot_response')
    list_filter = ('timestamp',)
    readonly_fields = ('timestamp',)
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    list_per_page = 25
    
    def short_user_message(self, obj):
        return obj.user_message[:50] + '...' if len(obj.user_message) > 50 else obj.user_message
    short_user_message.short_description = 'User Message'
    
    def short_bot_response(self, obj):
        return obj.bot_response[:50] + '...' if len(obj.bot_response) > 50 else obj.bot_response
    short_bot_response.short_description = 'Bot Response'
