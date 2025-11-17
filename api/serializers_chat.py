# Chat-related serializers
from rest_framework import serializers
from .models import ChatHistory, UserConversation, BotSettings, User

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatHistory
        fields = ['id', 'session_id', 'message', 'intent', 'response', 'timestamp']
        read_only_fields = ['timestamp']

class UserConversationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = UserConversation
        fields = ['id', 'user', 'username', 'user_message', 'bot_response', 'timestamp']
        read_only_fields = ['user', 'timestamp']

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
