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
from datetime import timedelta, datetime
from collections import Counter
import json

from .models import UserConversation, BotSettings, MoodAssessment, User, ChatThread
from .serializers_chat import (
    UserConversationSerializer, 
    ConversationSummarySerializer,
    BotSettingsSerializer,
    ChatThreadSerializer
)

THREAD_AUTO_DELETE_DAYS = 90
THREAD_MAX_COUNT = 50


def cleanup_expired_threads(user, days=THREAD_AUTO_DELETE_DAYS, max_threads=THREAD_MAX_COUNT):
    """Remove old or excess chat threads for a user."""
    if not user:
        return

    cutoff = timezone.now() - timedelta(days=days)
    ChatThread.objects.filter(user=user, updated_at__lt=cutoff).delete()

    active_threads = ChatThread.objects.filter(user=user, archived=False).order_by('-updated_at')
    if active_threads.count() > max_threads:
        thread_ids = list(active_threads.values_list('id', flat=True))[max_threads:]
        ChatThread.objects.filter(id__in=thread_ids).delete()


def derive_thread_title(user_message, bot_response):
    """Generate a short, human-readable title for a chat thread."""
    for raw_text in (user_message, bot_response):
        if not raw_text:
            continue
        line = raw_text.strip().split('\n')[0]
        if not line:
            continue
        return line[:57].rstrip() + ('...' if len(line) > 57 else '')
    return 'New Chat'


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
        thread_id = request.data.get('thread_id') or request.data.get('session_id')
        requested_title = request.data.get('thread_title')
        
        if not user_message:
            return Response(
                {"error": "Message cannot be empty"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            cleanup_expired_threads(request.user)

            thread = None
            if thread_id:
                thread = ChatThread.objects.filter(id=thread_id, user=request.user).first()

            if not thread:
                thread_title = (requested_title or '').strip() or 'New Chat'
                thread = ChatThread.objects.create(user=request.user, title=thread_title)

            # Get user's bot settings
            bot_settings, _ = BotSettings.objects.get_or_create(
                user=request.user,
                defaults={'bot_name': 'SereniAI'}
            )

            # Get conversation context
            context = self._get_conversation_context(request.user, thread)
            
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
                bot_response=bot_response,
                thread=thread
            )

            self._update_thread_metadata(thread, user_message, bot_response)

            return Response({
                "response": bot_response,
                "conversation_id": conversation.id,
                "thread_id": thread.id,
                "session_id": str(thread.id),
                "intent": intent,
                "context_used": len(context['recent_messages']) > 0
            }, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": f"An error occurred: {str(e)}"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _update_thread_metadata(self, thread, user_message, bot_response):
        """Refresh thread title and timestamps based on the latest exchange."""
        if not thread:
            return

        new_title = derive_thread_title(user_message, bot_response)
        fields_to_update = set()

        if new_title and new_title != thread.title:
            thread.title = new_title
            fields_to_update.add('title')

        if thread.expires_at and thread.expires_at < timezone.now():
            thread.expires_at = None
            fields_to_update.add('expires_at')

        fields_to_update.add('updated_at')
        thread.save(update_fields=list(fields_to_update))

    def _get_conversation_context(self, user, thread=None, limit=10):
        """
        Retrieve recent conversation history for context
        """
        recent_conversations = UserConversation.objects.filter(user=user)

        if thread:
            recent_conversations = recent_conversations.filter(thread=thread)

        recent_conversations = recent_conversations.order_by('-timestamp')[:limit]

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
        thread_id = request.query_params.get('thread_id')

        base_queryset = UserConversation.objects.filter(user=request.user)
        selected_thread = None

        if thread_id:
            selected_thread = ChatThread.objects.filter(id=thread_id, user=request.user).first()
            if selected_thread:
                base_queryset = base_queryset.filter(thread=selected_thread)
        
        conversations = base_queryset.order_by('-timestamp')[offset:offset+limit]
        
        serializer = UserConversationSerializer(conversations, many=True)
        total_count = base_queryset.count()

        thread_payload = ChatThreadSerializer(selected_thread).data if selected_thread else None

        return Response({
            'conversations': serializer.data,
            'total': total_count,
            'limit': limit,
            'offset': offset,
            'thread': thread_payload
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
        thread_id = request.query_params.get('thread_id')
        include_archived = request.query_params.get('include_archived') == 'true'

        conversations = UserConversation.objects.filter(user=request.user)
        selected_thread = None

        if thread_id:
            selected_thread = ChatThread.objects.filter(id=thread_id, user=request.user).first()
            if selected_thread:
                conversations = conversations.filter(thread=selected_thread)
            else:
                conversations = conversations.none()
        elif not include_archived:
            conversations = conversations.filter(Q(thread__archived=False) | Q(thread__isnull=True))
        
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
        recent_messages = []
        for conv in conversations[:50]:
            if conv.user_message:
                recent_messages.append(conv.user_message.lower())

        all_messages = ' '.join(recent_messages)
        
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

        payload = {
            'total_conversations': total,
            'recent_conversations_7days': recent,
            'main_topics': detected_topics[:5],
            'last_conversation_date': last_conversation.timestamp,
            'average_conversations_per_week': recent,
            'engagement_trend': 'increasing' if recent > 3 else 'moderate'
        }

        if selected_thread:
            payload['thread'] = ChatThreadSerializer(selected_thread).data

        return Response(payload, status=status.HTTP_200_OK)


class DeleteConversationView(APIView):
    """
    Delete specific conversation or all conversations
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, conversation_id=None):
        """
        Delete conversation(s)
        """
        thread_id = request.query_params.get('thread_id')

        if thread_id and not conversation_id:
            thread = ChatThread.objects.filter(id=thread_id, user=request.user).first()
            if not thread:
                return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

            message_count = thread.messages.count()
            thread.delete()
            return Response({
                'message': f'Thread deleted successfully',
                'messages_removed': message_count
            }, status=status.HTTP_200_OK)

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
            # Delete all conversations and threads for the user
            deleted_threads = ChatThread.objects.filter(user=request.user).delete()[0]
            deleted_messages = UserConversation.objects.filter(user=request.user).delete()[0]
            return Response({
                'message': f'{deleted_messages} conversations deleted successfully',
                'threads_removed': deleted_threads
            }, status=status.HTTP_200_OK)


class ConversationLogView(APIView):
    """Create conversation entries for externally generated responses."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_message = request.data.get('user_message', '').strip()
        bot_response = request.data.get('bot_response', '').strip()
        thread_id = request.data.get('thread_id') or request.data.get('session_id')
        requested_title = request.data.get('thread_title')

        if not user_message or not bot_response:
            return Response(
                {"error": "user_message and bot_response are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        cleanup_expired_threads(request.user)

        thread = None
        if thread_id:
            thread = ChatThread.objects.filter(id=thread_id, user=request.user).first()

        if not thread:
            thread_title = (requested_title or '').strip() or 'New Chat'
            thread = ChatThread.objects.create(user=request.user, title=thread_title)

        conversation = UserConversation.objects.create(
            user=request.user,
            user_message=user_message,
            bot_response=bot_response,
            thread=thread
        )

        self._update_thread_metadata(thread, user_message, bot_response)

        return Response(
            {
                "conversation_id": conversation.id,
                "timestamp": conversation.timestamp,
                "thread_id": thread.id
            },
            status=status.HTTP_201_CREATED
        )


class ChatThreadListCreateView(APIView):
    """List and create chat threads."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        include_archived = request.query_params.get('include_archived') == 'true'
        cleanup_expired_threads(request.user)

        threads = ChatThread.objects.filter(user=request.user)
        if not include_archived:
            threads = threads.filter(archived=False)

        threads = threads.order_by('-updated_at')
        serializer = ChatThreadSerializer(threads, many=True)
        return Response({'threads': serializer.data}, status=status.HTTP_200_OK)

    def post(self, request):
        cleanup_expired_threads(request.user)
        title = (request.data.get('title') or '').strip() or 'New Chat'
        thread = ChatThread.objects.create(user=request.user, title=title)
        serializer = ChatThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request):
        deleted_threads = ChatThread.objects.filter(user=request.user).delete()[0]
        deleted_messages = UserConversation.objects.filter(user=request.user).delete()[0]
        return Response({
            'message': 'All threads deleted successfully',
            'threads_removed': deleted_threads,
            'messages_removed': deleted_messages
        }, status=status.HTTP_200_OK)


class ChatThreadDetailView(APIView):
    """Retrieve or update a specific chat thread."""
    permission_classes = [IsAuthenticated]

    def get_thread(self, request, thread_id):
        return ChatThread.objects.filter(id=thread_id, user=request.user).first()

    def get(self, request, thread_id):
        thread = self.get_thread(request, thread_id)
        if not thread:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ChatThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, thread_id):
        thread = self.get_thread(request, thread_id)
        if not thread:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        updated = False

        if 'title' in request.data:
            new_title = (request.data['title'] or '').strip()
            if new_title:
                thread.title = new_title
                updated = True

        if 'archived' in request.data:
            thread.archived = bool(request.data['archived'])
            updated = True

        if 'expires_at' in request.data:
            expires_at_value = request.data['expires_at']
            if not expires_at_value:
                thread.expires_at = None
            else:
                try:
                    parsed = datetime.fromisoformat(expires_at_value)
                    if parsed.tzinfo is None:
                        parsed = timezone.make_aware(parsed, timezone.get_current_timezone())
                    thread.expires_at = parsed
                except ValueError:
                    return Response({'error': 'Invalid expires_at format. Use ISO8601.'}, status=status.HTTP_400_BAD_REQUEST)
            updated = True

        if updated:
            thread.save()

        serializer = ChatThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, thread_id):
        thread = self.get_thread(request, thread_id)
        if not thread:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        message_count = thread.messages.count()
        thread.delete()
        return Response({
            'message': 'Thread deleted successfully',
            'messages_removed': message_count
        }, status=status.HTTP_200_OK)


class ChatThreadMessagesView(APIView):
    """Fetch messages for a specific chat thread."""
    permission_classes = [IsAuthenticated]

    def get(self, request, thread_id):
        limit = int(request.query_params.get('limit', 50))
        offset = int(request.query_params.get('offset', 0))

        thread = ChatThread.objects.filter(id=thread_id, user=request.user).first()
        if not thread:
            return Response({'error': 'Thread not found'}, status=status.HTTP_404_NOT_FOUND)

        messages_qs = thread.messages.order_by('timestamp')
        total = messages_qs.count()
        paginated = messages_qs[offset:offset+limit]

        serializer = UserConversationSerializer(paginated, many=True)

        return Response({
            'thread': ChatThreadSerializer(thread).data,
            'messages': serializer.data,
            'total': total,
            'limit': limit,
            'offset': offset
        }, status=status.HTTP_200_OK)
