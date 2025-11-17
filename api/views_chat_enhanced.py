"""
Enhanced Chatbot Views with Context Awareness and History
This module provides improved AI chatbot functionality with:
- Conversation history storage and retrieval
- Context-aware responses based on user history
- User profile and mood analysis
- Personalized recommendations
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from collections import Counter
import json

from .models import UserConversation, BotSettings, MoodAssessment, User
from .serializers_chat import (
    UserConversationSerializer, 
    ConversationSummarySerializer,
    BotSettingsSerializer
)


class EnhancedChatView(APIView):
    """
    Enhanced chatbot endpoint with context awareness and history
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Process user message with context from conversation history
        """
        user_message = request.data.get('message', '').strip()
        session_id = request.data.get('session_id', None)
        
        if not user_message:
            return Response(
                {"error": "Message cannot be empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Get user's bot settings
            bot_settings, _ = BotSettings.objects.get_or_create(
                user=request.user,
                defaults={'bot_name': 'SereniAI'}
            )

            # Get conversation context
            context = self._get_conversation_context(request.user)
            
            # Get recent mood assessments
            mood_context = self._get_mood_context(request.user)
            
            # Analyze user message with context
            intent, sentiment = self._analyze_message(user_message, context)
            
            # Generate contextual response
            bot_response = self._generate_response(
                user_message=user_message,
                intent=intent,
                sentiment=sentiment,
                context=context,
                mood_context=mood_context,
                bot_name=bot_settings.bot_name,
                user=request.user
            )

            # Save conversation
            conversation = UserConversation.objects.create(
                user=request.user,
                user_message=user_message,
                bot_response=bot_response
            )

            return Response({
                "response": bot_response,
                "conversation_id": conversation.id,
                "session_id": session_id or str(conversation.id),
                "intent": intent,
                "context_used": len(context['recent_messages']) > 0
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _get_conversation_context(self, user, limit=10):
        """
        Retrieve recent conversation history for context
        """
        recent_conversations = UserConversation.objects.filter(
            user=user
        ).order_by('-timestamp')[:limit]

        messages = []
        topics = []
        
        for conv in recent_conversations:
            messages.append({
                'user': conv.user_message,
                'bot': conv.bot_response,
                'timestamp': conv.timestamp
            })
            
        return {
            'recent_messages': messages,
            'message_count': len(messages),
            'topics': topics
        }

    def _get_mood_context(self, user):
        """
        Get recent mood assessments to understand user's state
        """
        recent_moods = MoodAssessment.objects.filter(
            user=user,
            timestamp__gte=timezone.now() - timedelta(days=30)
        ).order_by('-timestamp')[:5]

        if not recent_moods:
            return None

        mood_data = {
            'avg_happiness': sum(m.happiness for m in recent_moods) / len(recent_moods),
            'avg_stress': sum(m.stress_level for m in recent_moods) / len(recent_moods),
            'avg_sleep': sum(m.sleep_quality for m in recent_moods) / len(recent_moods),
            'anxiety_levels': [m.anxiety for m in recent_moods],
            'energy_levels': [m.energy for m in recent_moods],
            'last_assessment': recent_moods[0].timestamp if recent_moods else None
        }

        return mood_data

    def _analyze_message(self, message, context):
        """
        Analyze user message for intent and sentiment
        """
        message_lower = message.lower()
        
        # Intent detection
        intents = {
            'crisis': ['suicide', 'kill myself', 'end it all', 'want to die', 'hurt myself'],
            'anxiety': ['anxious', 'panic', 'worried', 'nervous', 'stressed', 'overwhelming'],
            'depression': ['depressed', 'sad', 'hopeless', 'lonely', 'empty', 'worthless'],
            'sleep': ['sleep', 'insomnia', 'tired', 'exhausted', 'cant sleep'],
            'relationship': ['relationship', 'family', 'friend', 'partner', 'spouse'],
            'work_stress': ['work', 'job', 'boss', 'career', 'colleague'],
            'coping': ['cope', 'handle', 'deal with', 'manage', 'overcome'],
            'progress': ['better', 'improving', 'progress', 'feeling good'],
            'greeting': ['hi', 'hello', 'hey', 'good morning', 'good evening'],
            'gratitude': ['thank', 'thanks', 'appreciate', 'grateful'],
            'goodbye': ['bye', 'goodbye', 'see you', 'talk later', 'gotta go']
        }

        detected_intent = 'general'
        for intent, keywords in intents.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_intent = intent
                break

        # Sentiment analysis (simplified)
        positive_words = ['good', 'better', 'great', 'happy', 'improving', 'helped']
        negative_words = ['bad', 'worse', 'terrible', 'awful', 'horrible', 'struggling']
        
        sentiment_score = sum(1 for word in positive_words if word in message_lower)
        sentiment_score -= sum(1 for word in negative_words if word in message_lower)
        
        if sentiment_score > 0:
            sentiment = 'positive'
        elif sentiment_score < 0:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'

        return detected_intent, sentiment

    def _generate_response(self, user_message, intent, sentiment, context, mood_context, bot_name, user):
        """
        Generate contextual response based on message, history, and user state
        """
        responses = {
            'crisis': [
                f"I'm really concerned about what you're sharing, {user.first_name or user.username}. Your safety is the most important thing right now. Please reach out to a crisis helpline immediately:\n\n"
                "🆘 National Suicide Prevention Lifeline: 988\n"
                "🆘 Crisis Text Line: Text HOME to 741741\n\n"
                "You don't have to go through this alone. Please talk to a professional who can help you right now.",
                
                f"{user.first_name or user.username}, I hear that you're in a lot of pain right now, and I want you to know that your life matters. "
                "Please contact emergency services or a crisis helpline:\n\n"
                "🆘 Call 988 (Suicide & Crisis Lifeline)\n"
                "🆘 Text HOME to 741741\n"
                "🆘 Or call 911 for immediate help\n\n"
                "There are people who want to help you through this. Please reach out right now."
            ],
            'anxiety': [
                f"I can sense you're feeling anxious, {user.first_name or user.username}. Let's try a quick grounding exercise:\n\n"
                "🌟 Take a slow, deep breath in for 4 counts\n"
                "🌟 Hold it for 4 counts\n"
                "🌟 Breathe out for 6 counts\n\n"
                "Repeat this 3-5 times. " + self._add_historical_context(context, 'anxiety'),
                
                f"{user.first_name or user.username}, anxiety can feel overwhelming, but you can get through this. "
                "What specific thoughts or situations are triggering your anxiety right now? " +
                self._add_mood_insight(mood_context, 'anxiety')
            ],
            'depression': [
                f"Thank you for sharing how you're feeling, {user.first_name or user.username}. Depression can make everything feel heavy. "
                "Remember that what you're experiencing is valid, and things can get better. " +
                self._add_historical_context(context, 'depression') +
                "\n\nHave you considered talking to a mental health professional? I can help you find resources.",
                
                f"{user.first_name or user.username}, I hear that you're going through a difficult time. "
                "Even small steps matter - have you been able to do anything today that made you feel even slightly better? " +
                self._add_mood_insight(mood_context, 'depression')
            ],
            'sleep': [
                f"Sleep issues can really affect how we feel, {user.first_name or user.username}. " +
                self._add_mood_insight(mood_context, 'sleep') +
                "\n\nHere are some tips that might help:\n"
                "💤 Keep a consistent sleep schedule\n"
                "💤 Avoid screens 30 minutes before bed\n"
                "💤 Create a relaxing bedtime routine\n"
                "💤 Keep your bedroom cool and dark\n\n"
                "How long have you been experiencing sleep difficulties?"
            ],
            'relationship': [
                f"Relationships can be complex, {user.first_name or user.username}. Tell me more about what's happening. "
                "Is this about a specific conflict, or more of an ongoing pattern? " +
                self._add_historical_context(context, 'relationship')
            ],
            'progress': [
                f"That's wonderful to hear, {user.first_name or user.username}! 🌟 I'm so glad you're feeling better. "
                "What do you think has been helping you make this progress? " +
                self._celebrate_progress(context, mood_context)
            ],
            'gratitude': [
                f"You're very welcome, {user.first_name or user.username}! I'm here whenever you need support. "
                "Taking time to talk about your feelings is a sign of strength. Keep taking care of yourself! 💚"
            ],
            'goodbye': [
                f"Take care, {user.first_name or user.username}! Remember, I'm here 24/7 whenever you need to talk. "
                "Be kind to yourself. 💚",
                
                f"Goodbye, {user.first_name or user.username}. You're doing great by reaching out. "
                "Don't hesitate to come back anytime. Wishing you peace and wellness! 🌟"
            ]
        }

        # Get response for detected intent
        if intent in responses and responses[intent]:
            import random
            response = random.choice(responses[intent])
        else:
            # Default contextual response
            response = self._generate_default_response(user, user_message, context, mood_context, bot_name)

        return response

    def _add_historical_context(self, context, topic):
        """
        Add relevant context from conversation history
        """
        if context['message_count'] > 0:
            return f"\n\nI notice we've talked before about similar feelings. Remember, you're making progress just by continuing to reach out."
        return ""

    def _add_mood_insight(self, mood_context, topic):
        """
        Add insights based on mood assessment history
        """
        if not mood_context:
            return ""

        insights = []
        
        if topic == 'anxiety' and mood_context['avg_stress'] > 7:
            insights.append("I've noticed your stress levels have been high recently.")
        elif topic == 'depression' and mood_context['avg_happiness'] < 4:
            insights.append("Your recent mood assessments show you've been struggling.")
        elif topic == 'sleep' and mood_context['avg_sleep'] < 5:
            insights.append("Your sleep quality has been lower than ideal lately.")

        if insights:
            return "\n\n" + " ".join(insights)
        return ""

    def _celebrate_progress(self, context, mood_context):
        """
        Celebrate user progress based on history
        """
        if mood_context and mood_context['avg_happiness'] > 6:
            return "\n\nYour mood assessments show real improvement - that's something to be proud of!"
        return ""

    def _generate_default_response(self, user, user_message, context, mood_context, bot_name):
        """
        Generate a thoughtful default response
        """
        greeting = f"I'm listening, {user.first_name or user.username}."
        
        if context['message_count'] > 5:
            greeting += " I remember our previous conversations, and I'm here to continue supporting you."
        
        return (
            f"{greeting}\n\n"
            f"Tell me more about what's on your mind. I'm here to listen without judgment and help you work through whatever you're experiencing. "
            f"Your thoughts and feelings are valid and important."
        )


class ConversationHistoryView(APIView):
    """
    Retrieve user's conversation history
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Get conversation history with pagination
        """
        limit = int(request.query_params.get('limit', 20))
        offset = int(request.query_params.get('offset', 0))
        
        conversations = UserConversation.objects.filter(
            user=request.user
        ).order_by('-timestamp')[offset:offset+limit]

        serializer = UserConversationSerializer(conversations, many=True)
        
        total_count = UserConversation.objects.filter(user=request.user).count()

        return Response({
            'conversations': serializer.data,
            'total': total_count,
            'limit': limit,
            'offset': offset
        }, status=status.HTTP_200_OK)


class ConversationAnalyticsView(APIView):
    """
    Get analytics and insights from conversation history
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Provide conversation analytics and insights
        """
        conversations = UserConversation.objects.filter(user=request.user)
        
        if not conversations.exists():
            return Response({
                'message': 'No conversation history yet',
                'total_conversations': 0
            }, status=status.HTTP_200_OK)

        # Analytics
        total = conversations.count()
        recent = conversations.filter(
            timestamp__gte=timezone.now() - timedelta(days=7)
        ).count()
        
        last_conversation = conversations.latest('timestamp')
        
        # Simple topic extraction (you can enhance this with NLP)
        all_messages = ' '.join([c.user_message.lower() for c in conversations[:50]])
        
        topic_keywords = {
            'anxiety': ['anxious', 'worry', 'panic', 'nervous'],
            'depression': ['sad', 'depressed', 'hopeless', 'lonely'],
            'sleep': ['sleep', 'insomnia', 'tired'],
            'stress': ['stress', 'overwhelm', 'pressure'],
            'relationships': ['relationship', 'family', 'friend']
        }
        
        detected_topics = []
        for topic, keywords in topic_keywords.items():
            if any(keyword in all_messages for keyword in keywords):
                detected_topics.append(topic)

        return Response({
            'total_conversations': total,
            'recent_conversations_7days': recent,
            'main_topics': detected_topics[:5],
            'last_conversation_date': last_conversation.timestamp,
            'average_conversations_per_week': recent,
            'engagement_trend': 'increasing' if recent > 3 else 'moderate'
        }, status=status.HTTP_200_OK)


class DeleteConversationView(APIView):
    """
    Delete specific conversation or all conversations
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, conversation_id=None):
        """
        Delete conversation(s)
        """
        if conversation_id:
            # Delete specific conversation
            try:
                conversation = UserConversation.objects.get(
                    id=conversation_id,
                    user=request.user
                )
                conversation.delete()
                return Response({
                    'message': 'Conversation deleted successfully'
                }, status=status.HTTP_200_OK)
            except UserConversation.DoesNotExist:
                return Response({
                    'error': 'Conversation not found'
                }, status=status.HTTP_404_NOT_FOUND)
        else:
            # Delete all conversations
            count = UserConversation.objects.filter(user=request.user).delete()[0]
            return Response({
                'message': f'{count} conversations deleted successfully'
            }, status=status.HTTP_200_OK)
