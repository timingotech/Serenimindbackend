from rest_framework import serializers
from .models import UserProfile
from .models import Post
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import JournalEntry
from .models import Community
from .models import Message
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import UserSettings
from .models import Todo, MoodEntry
from rest_framework import serializers
from .models import MoodAssessment
from rest_framework import serializers
from .models import BotSettings

class BotSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BotSettings
        fields = ['bot_name']
        
        
class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class MoodEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodEntry
        fields = '__all__'
        
class UserSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSettings
        fields = ['email_notifications', 'push_notifications', 'sms_notifications', 'profile_visibility', 'search_visibility', 'current_theme']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        
class UserProfile(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['firstName', 'lastName', 'username', 'email', 'whyHere']

    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # Add more fields as needed, such as password confirmation, etc.

    def validate_email(self, value):
        # Additional validation logic for the email field
        # For example, checking if the email exists in the database
        return value

    def save(self):
        # Perform any necessary actions, such as sending a password reset email
        pass


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user', 'message', 'timestamp']

class JournalEntrySerializer(serializers.ModelSerializer):
    # Example read-only field
    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        model = JournalEntry
        fields = '__all__'

    def create(self, validated_data):
        # Custom creation logic if needed
        return JournalEntry.objects.create(**validated_data)
    
class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        print(token)
        # ...  

        return token

class SenderIdSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=Message.objects.all(), source='user')

    class Meta:
        model = Message
        fields = ['user_id']
        

class MoodAssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoodAssessment
        fields = '__all__'
        read_only_fields = ('user', 'timestamp')