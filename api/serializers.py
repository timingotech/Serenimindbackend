from rest_framework import serializers
from .models import UserProfile
from .models import Post
from rest_framework import serializers
from django.contrib.auth.models import User

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