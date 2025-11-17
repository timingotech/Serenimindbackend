# Chat-related serializers
from rest_framework import serializers
from .models import ChatHistory, UserConversation, BotSettings, User, ChatThread

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'session_id', 'message', 'intent', 'response', 'timestamp']
        read_only_fields = ['timestamp']

class UserConversationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = UserConversation
        fields = ['id', 'user', 'username', 'user_message', 'bot_response', 'timestamp', 'thread']
        read_only_fields = ['user', 'timestamp']

    def get_username(self, obj):
        user = getattr(obj, 'user', None)
        if user and hasattr(user, 'username'):
            return user.username
        return None


class ChatThreadSerializer(serializers.ModelSerializer):
    message_count = serializers.SerializerMethodField()
    last_message_preview = serializers.SerializerMethodField()

    class Meta:
        model = ChatThread
        fields = [
            'id',
            'title',
            'archived',
            'created_at',
            'updated_at',
            'expires_at',
            'message_count',
            'last_message_preview'
        ]
        read_only_fields = [
            'archived',
            'created_at',
            'updated_at',
            'expires_at',
            'message_count',
            'last_message_preview'
        ]

    def get_message_count(self, obj):
        return obj.messages.count()

    def get_last_message_preview(self, obj):
        latest_entry = obj.messages.order_by('-timestamp').first()
        if not latest_entry:
            return None
        candidate = latest_entry.bot_response or latest_entry.user_message
        if not candidate:
            return None
        candidate = candidate.strip()
        return candidate[:80] + ('...' if len(candidate) > 80 else '')

class BotSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotSettings
        fields = ['id', 'user', 'bot_name', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

class ConversationSummarySerializer(serializers.Serializer):
    """Serializer for conversation analytics"""
    total_conversations = serializers.IntegerField()
    recent_topics = serializers.ListField(child=serializers.CharField())
    mood_trends = serializers.ListField(child=serializers.CharField())
    last_conversation = serializers.DateTimeField()
