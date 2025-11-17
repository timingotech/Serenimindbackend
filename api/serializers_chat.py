# Chat-related serializers
from rest_framework import serializers
from .models import ChatHistory, UserConversation, BotSettings, User

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'session_id', 'message', 'intent', 'response', 'timestamp']
        read_only_fields = ['timestamp']

class UserConversationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = UserConversation
        fields = ['id', 'user', 'username', 'user_message', 'bot_response', 'timestamp']
        read_only_fields = ['user', 'timestamp']

    def get_username(self, obj):
        user = getattr(obj, 'user', None)
        if user and hasattr(user, 'username'):
            return user.username
        return None

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
