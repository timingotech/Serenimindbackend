from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from rest_framework import status
from .serializers import UserProfile
from django.views.decorators.csrf import csrf_exempt
import requests
from .models import Report
from .models import UserProfile
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Todo, MoodEntry
from .serializers import TodoSerializer, MoodEntrySerializer
import random
from .models import Community
from django.http import JsonResponse, HttpResponseBadRequest
import string
from .models import BlogPost  # Import your BlogPost model
from .serializers import SenderIdSerializer
from django.core.mail import send_mail
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from rest_framework import viewsets
from .models import Community
from .serializers import CommunitySerializer
from django.middleware.csrf import get_token
from django.http import JsonResponse
from django.views.decorators.csrf import requires_csrf_token
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from rest_framework import generics
from .models import CommunityPost
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail, EmailMessage
from .serializers import CommunitySerializer
from django.core.cache import cache
from django.contrib.auth.models import User
from django.http import JsonResponse
import jwt
import datetime
import os
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from .models import Message
from .serializers import MessageSerializer
from .models import Message
from .serializers import MessageSerializer, MyTokenObtainPairSerializer
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView
from django.contrib.auth.forms import PasswordResetForm
from .serializers import PasswordResetSerializer     
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import UserProfile
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserSettings
from .serializers import UserSettingsSerializer
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Post
from .serializers import PostSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from .models import JournalEntry
from .serializers import MoodAssessmentSerializer
from .serializers import JournalEntrySerializer
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Conversation, AIMessage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import random
from collections import Counter
from rest_framework.views import APIView
from rest_framework.response import Response

# Download required NLTK data
NLTK_DATA_PATH = '/opt/render/punkt'
if not os.path.exists(NLTK_DATA_PATH):
    os.makedirs(NLTK_DATA_PATH)

nltk.data.path.append(NLTK_DATA_PATH)

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('corpora/stopwords')
    NLTK_DATA_AVAILABLE = True
except LookupError:
    nltk.download('punkt', download_dir=NLTK_DATA_PATH)
    nltk.download('stopwords', download_dir=NLTK_DATA_PATH)
    NLTK_DATA_AVAILABLE = True

class ChatbotView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_or_train_model()
        self.intents = {
            'greeting': ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening', 'howdy', 'greetings'],
    'farewell': ['bye', 'goodbye', 'see you later', 'take care', 'farewell', 'until next time', 'catch you later'],
    'thanks': ['thank you', 'thanks', 'appreciate it', 'grateful', 'much obliged', 'cheers'],
    'help': ['help', 'can you help me', 'I need assistance', 'support', 'guidance', 'aid', 'what can you do'],
    'feeling_good': ["I feel good", "I'm happy", 'feeling great', 'excited', 'joyful', 'content', 'on top of the world'],
    'feeling_bad': ["I feel bad", "I'm sad", 'feeling down', 'depressed', 'unhappy', 'miserable', 'gloomy', 'anxious'],
    'stress': ['stressed', 'overwhelmed', 'under pressure', 'burnout', 'can\'t cope', 'too much to handle'],
    'sleep_issues': ['can\'t sleep', 'insomnia', 'trouble sleeping', 'wake up tired', 'nightmares', 'sleep problems'],
    'relationship': ['relationship problems', 'breakup', 'divorce', 'family issues', 'friend trouble', 'loneliness'],
    'work': ['job stress', 'career change', 'workplace issues', 'unemployment', 'work-life balance'],
    'health': ['health concerns', 'illness', 'chronic pain', 'disability', 'medical anxiety'],
    'self_improvement': ['want to improve', 'self-development', 'personal growth', 'learning', 'new skills'],
    'meditation': ['how to meditate', 'mindfulness', 'relaxation techniques', 'calm my mind'],
    'exercise': ['workout routine', 'stay fit', 'exercise motivation', 'physical activity'],
    'nutrition': ['healthy eating', 'diet advice', 'nutritional information', 'food and mood'],
    'motivation': ['lack motivation', 'how to stay motivated', 'setting goals', 'achieving objectives'],
    'anger': ['anger management', 'feeling frustrated', 'how to control temper', 'dealing with rage'],
    'anxiety': ['feeling anxious', 'panic attacks', 'social anxiety', 'worry too much'],
    'depression': ['dealing with depression', 'feeling hopeless', 'loss of interest', 'persistent sadness'],
    'ai_companion': ['AI friend', 'talk to AI', 'SereniAI features', 'AI support', 'how can AI help me'],
    'community_support': ['join community', 'support groups', 'connect with others', 'share experiences', 'community features'],
    'journaling': ['personal journal', 'how to journal', 'reflection techniques', 'track progress', 'journal features'],
    'mood_boosting_activities': ['fun activities', 'games for mood', 'mood improvement', 'feel better activities', 'uplift spirits'],
    'blog_posts': ['read blogs', 'inspiring articles', 'write a blog', 'motivational content', 'positive reading'],
    'daily_inspiration': ['daily quotes', 'morning motivation', 'inspirational messages', 'positive reminders', 'daily encouragement'],
    'platform_info': ['SereniMind features', 'what services do you offer', 'how can SereniMind help me', 'tell me about SereniMind', 'what is SereniMind'],
    'question': ['can you explain','why','what','how'],
    }

    def load_or_train_model(self):
        model_path = 'model.pkl'
        # Check if model already exists
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
            except (FileNotFoundError, pickle.UnpicklingError) as e:
                print(f"Error loading model: {e}")
                self.train_model()  # Train the model if loading fails
        else:
            self.train_model()

    def train_model(self):
        # Tokenization and stopword removal using NLTK
        if NLTK_DATA_AVAILABLE:
            stop_words = set(stopwords.words('english'))
        else:
            stop_words = set()  # In case NLTK data isn't available

        all_texts = []
        all_labels = []
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                tokens = word_tokenize(phrase.lower())
                filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
                all_texts.append(' '.join(filtered_tokens))
                all_labels.append(intent)

        # Vectorization using TF-IDF
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(all_texts)

        # Training a simple logistic regression model
        model = LogisticRegression()
        model.fit(X, all_labels)

        self.model = (model, vectorizer)  # Save both the model and vectorizer

        # Save the model to a file
        with open('model.pkl', 'wb') as f:
            pickle.dump((model, vectorizer), f)

    def post(self, request):
        # Updated responses for each intent with multiple options
        responses = {
            'greeting': [
        'Hello! How can I assist you today?',
        'Hi there! How are you feeling?',
        'Greetings! What brings you to our chat today?',
        'Good to see you! How has your day been so far?',
        'Welcome! Is there anything specific on your mind?'
    ],
    'farewell': [
        "Goodbye! Take care and remember, you're stronger than you think.",
        "See you later. Remember, I'm here if you need to talk.",
        "Farewell for now. Stay positive and keep moving forward!",
        "Until next time! Don't forget to practice self-care.",
        "Take care! Remember, every day is a new opportunity."
    ],
    'thanks': [
        "You're welcome! I'm glad I could help.",
        "It's my pleasure. Remember, you're doing great!",
        "I'm happy to assist. Keep up the good work!",
        "Anytime! Your well-being is important to me.",
        "No need to thank me. You're the one doing the hard work!"
    ],
    'help': [
        "I'm here to help. What's on your mind?",
        "How can I assist you today? I'm all ears.",
        "I'm here to support you. What would you like to talk about?",
        "Let's work through this together. What's troubling you?",
        "I'm your AI companion, ready to help. What do you need?"
    ],
    'feeling_good': [
        "That's wonderful to hear! What's contributing to your positive mood?",
        "I'm so glad you're feeling good. What's been going well for you?",
        "It's great that you're in a good mood! How can we maintain this positive energy?",
        "Fantastic! Positive feelings are worth celebrating. What's making you feel this way?",
        "That's excellent! Let's build on this positive feeling. What's your next goal?"
    ],
    'feeling_bad': [
        "I'm sorry to hear that. Would you like to talk about what's bothering you?",
        "It's okay to feel down sometimes. Can you tell me more about what's going on?",
        "I'm here to listen. What do you think is causing these negative feelings?",
        "Your feelings are valid. Let's explore what's troubling you and see if we can find a way forward.",
        "Thank you for sharing. It takes courage to admit when we're not feeling our best. How can I support you?"
    ],
    'question': [
        "That's an interesting question. Can you provide more context?",
        "I'd be happy to help answer that. Could you give me more details?",
        "Great question! Let's explore that together. What specifically would you like to know?",
        "Questions are the first step to understanding. Can you elaborate on what you're asking?",
        "I'm here to help you find answers. Can you tell me more about what prompted this question?"
    ],
    'stress': [
        "It sounds like you're under a lot of pressure. Let's talk about some stress management techniques.",
        "Feeling overwhelmed is common. Have you tried any relaxation exercises?",
        "Stress can be challenging. Would you like to explore some coping strategies together?",
        "I hear you're feeling stressed. Let's break down what's causing this and address each part.",
        "Managing stress is important for your well-being. How about we discuss some self-care practices?"
    ],
    'sleep_issues': [
        "Sleep problems can be frustrating. Have you established a regular sleep routine?",
        "Trouble sleeping can affect your whole day. Let's talk about some sleep hygiene tips.",
        "Insomnia can be challenging. Have you considered trying relaxation techniques before bed?",
        "Sleep is crucial for mental health. Would you like to explore some natural sleep aids?",
        "Waking up tired can be tough. Let's discuss ways to improve your sleep quality."
    ],
    'relationship': [
        "Relationship challenges can be difficult. Would you like to talk more about what's happening?",
        "I'm sorry you're experiencing relationship troubles. How long has this been going on?",
        "Relationship issues can be complex. Have you considered couples counseling?",
        "It's brave of you to address your relationship concerns. What do you think is at the root of the problem?",
        "Navigating relationships can be tough. Let's discuss some communication strategies that might help."
    ],
    'work': [
        "Work-related stress is common. How do you usually cope with job pressure?",
        "Career changes can be both exciting and scary. What's motivating this change?",
        "Balancing work and life can be challenging. Would you like to explore some time management techniques?",
        "I'm sorry to hear about your workplace issues. Have you spoken with HR or a supervisor about this?",
        "Unemployment can be stressful. Let's talk about strategies for job searching and maintaining positivity."
    ],
    'health': [
        "Health concerns can be worrying. Have you consulted with a healthcare professional about this?",
        "Chronic pain can be challenging to manage. Are you interested in discussing some pain management techniques?",
        "I understand your health anxiety. Would you like to explore some ways to manage these feelings?",
        "Living with a disability presents unique challenges. How can I support you in navigating this?",
        "Your health is important. Let's talk about ways to prioritize your well-being while managing your condition."
    ],
    'self_improvement': [
        "It's great that you want to improve yourself! What specific areas are you looking to develop?",
        "Personal growth is a journey. What inspired you to focus on self-improvement?",
        "Learning new skills can be exciting. Do you have any specific goals in mind?",
        "Self-development is a positive step. How do you plan to track your progress?",
        "It's admirable that you're focusing on personal growth. What's the first small step you can take today?"
    ],
    'meditation': [
        "Meditation can be a powerful tool for mental health. Have you tried any guided meditation apps?",
        "Mindfulness practices can help calm the mind. Would you like to try a short breathing exercise?",
        "Learning to meditate takes time and patience. What has been your experience so far?",
        "Relaxation techniques can be very beneficial. Are you interested in learning about progressive muscle relaxation?",
        "Calming the mind through meditation is a valuable skill. How about we start with a simple 5-minute mindfulness exercise?"
    ],
    'exercise': [
        "Regular exercise is great for both physical and mental health. What types of activities do you enjoy?",
        "Starting a workout routine can be challenging. How about we discuss some simple exercises to begin with?",
        "Staying motivated to exercise isn't always easy. Would you like to explore some strategies to keep yourself going?",
        "Physical activity is a great mood booster. Have you considered joining any sports or fitness classes?",
        "Finding time for exercise can be tough. Let's brainstorm some ways to incorporate more movement into your daily routine."
    ],
    'nutrition': [
        "Healthy eating plays a big role in overall well-being. Would you like to discuss some balanced meal ideas?",
        "Diet can significantly impact mood and energy levels. How would you describe your current eating habits?",
        "Nutritional information can be overwhelming. Are there specific areas of your diet you'd like to improve?",
        "The connection between food and mood is strong. Have you noticed any foods that seem to affect how you feel?",
        "Making dietary changes can be challenging. Let's start by talking about small, sustainable changes you can make."
    ],
    'motivation': [
        "Lack of motivation can be frustrating. What usually helps you feel motivated?",
        "Setting and achieving goals can boost motivation. Would you like to discuss goal-setting strategies?",
        "Sometimes motivation comes after we start acting. How about we break down your goal into smaller, manageable tasks?",
        "Staying motivated is an ongoing process. Have you tried using a reward system for accomplishing tasks?",
        "It's normal for motivation to fluctuate. Let's explore some techniques to help you stay on track with your objectives."
    ],
    'anger': [
        "Managing anger can be challenging. Have you identified any specific triggers for your anger?",
        "Learning to control your temper is a valuable skill. Would you like to discuss some anger management techniques?",
        "Feeling frequently frustrated can be tough. How do you typically express your anger?",
        "Dealing with rage in a healthy way is important. Let's talk about some strategies to help you cool down when you're angry.",
        "Anger often masks other emotions. Can we explore what might be beneath your anger?"
    ],
    'anxiety': [
        "Anxiety can be overwhelming. Have you tried any relaxation techniques to manage your anxiety?",
        "Feeling anxious is a common experience. Would you like to discuss some coping strategies?",
        "Panic attacks can be scary. Let's talk about some grounding techniques that might help during an attack.",
        "Social anxiety can be challenging. How does it typically affect your daily life?",
        "Excessive worry can be draining. Have you considered keeping a worry journal to track your anxious thoughts?"
    ],
    'depression': [
        "I'm sorry you're dealing with depression. Have you been able to talk to a mental health professional about how you're feeling?",
        "Feeling hopeless can be really tough. Can you tell me more about what's been going on?",
        "Loss of interest in activities is a common symptom of depression. Are there any activities you used to enjoy?",
        "Persistent sadness is difficult to handle alone. Would you like to explore some self-care strategies that might help?",
        "Depression is a serious condition, but there is hope. How can I support you in seeking help or treatment?"
    ],
    'unknown': [
        "I'm not sure I fully understand. Could you rephrase that or provide more details?",
        "I'm still learning and growing. Can you tell me more about what you mean?",
        "I want to make sure I'm addressing your needs correctly. Could you elaborate on that?",
        "I'm not quite sure how to respond to that. Can you give me some more context?",
        "I'm afraid I don't have enough information to respond accurately. Could you clarify your question or statement?"
    ],
    'seek_professional_help': [
        "It's great that you're considering professional help. SereniMind offers personalized guidance from experienced mental health professionals. Would you like me to guide you through booking a session?",
        "Seeking professional support is a strong and positive step. We have a range of experts available, from counselors to career coaches. Can I help you find the right professional for your needs?",
        "I'm glad you're reaching out for professional support. SereniMind's network of mental health professionals is here to help. What kind of support are you looking for?",
        "Professional guidance can be incredibly beneficial. SereniMind offers various types of professional support. Would you like to explore our counseling services?",
        "It's courageous to seek professional help. SereniMind can connect you with experienced therapists. Shall we look at available options together?"
    ],
    'ai_companion': [
        "As your AI companion, I'm here to offer support and a safe space for open conversations. How can I assist you today?",
        "SereniAI is designed to be your trusted AI friend, offering tailored support. What would you like to talk about?",
        "I'm your AI-powered confidant, here to listen and support you. Is there anything specific on your mind?",
        "As an AI companion, I'm here to offer a judgment-free space for you to express yourself. What would you like to discuss?",
        "SereniAI is here to provide personalized support. How can I make your day a little brighter?"
    ],
    'community_support': [
        "SereniMind offers a supportive community where you can connect with like-minded individuals. Would you like to learn more about our community features?",
        "Sharing experiences and growing together can be really beneficial. Our community provides a nurturing space for this. Are you interested in joining?",
        "The SereniMind community is a great place to find support and understanding. What kind of connections are you looking to make?",
        "Our supportive community is here to help you on your journey. Would you like to explore how you can engage with others who may have similar experiences?",
        "Connecting with others can be a powerful tool for growth. How about we take a look at the community features SereniMind offers?"
    ],
    'journaling': [
        "SereniMind offers a personal journal feature to help with self-discovery and tracking your progress. Would you like some tips on how to get started with journaling?",
        "Journaling can be a great tool for reflection and goal-setting. How about we explore some journaling prompts together?",
        "Our personalized journal is designed to help you reflect and grow. What aspects of journaling are you most interested in?",
        "Tracking your journey through journaling can be really insightful. Would you like to learn more about how to use SereniMind's journal feature effectively?",
        "Journaling is a powerful tool for self-discovery. Shall we discuss some techniques to make the most of your journaling practice?"
    ],
    'mood_boosting_activities': [
        "SereniMind offers a variety of mood-boosting activities. Would you like to try a game, listen to some uplifting sounds, or perhaps watch a motivational video?",
        "Engaging in fun activities can really help uplift your spirits. What kind of activity do you usually enjoy when you need a mood boost?",
        "We have exercises specifically designed to enrich your well-being. Are you in the mood for something active, creative, or relaxing?",
        "Mood-boosting activities can be a great way to shift your energy. Would you like to explore some of the options we have available?",
        "From games to exercises, we have various activities to help improve your mood. What sort of activity appeals to you right now?"
    ],
    'blog_posts': [
        "SereniMind features inspiring blog posts to keep you motivated. Would you like me to recommend a blog post based on how you're feeling today?",
        "Our platform allows you to both read and create uplifting blogs. Are you interested in reading some motivational content or perhaps sharing your own story?",
        "Engaging with positive content can help maintain focus on personal growth. What topics are you most interested in reading about?",
        "Our blog section is filled with inspiring stories and helpful tips. Would you like to explore some recent posts?",
        "Writing can be as therapeutic as reading. Would you like to try writing a short blog post about your experiences or read some uplifting content?"
    ],
    'daily_inspiration': [
        "SereniMind offers daily inspiration to start your day on a positive note. Would you like to hear today's motivational quote?",
        "Daily reminders can help keep you energized and focused. How about we set up personalized daily inspirational messages for you?",
        "Starting the day with inspiration can set a positive tone. What kind of motivational content resonates with you the most?",
        "Our daily inspiration feature is designed to boost your motivation. Would you like to customize the type of inspirational content you receive?",
        "Positive reminders throughout the day can be really helpful. Shall we explore how to make the most of SereniMind's daily inspiration feature?"
    ],
    'platform_info': [
        "SereniMind offers a range of features including professional support, AI companionship, community engagement, journaling, mood-boosting activities, inspiring blogs, and daily motivation. Which aspect would you like to know more about?",
        "Our platform is designed to support your mental well-being through various services. We offer everything from professional counseling to AI-powered conversations. What area of support are you most interested in?",
        "SereniMind is here to support your personal growth and mental health. We provide tools for self-reflection, community support, professional guidance, and more. How can we best assist you today?",
        "From AI companionship to professional therapy, SereniMind offers comprehensive support for your mental well-being. Would you like an overview of our key features?",
        "SereniMind is your all-in-one platform for mental health support. We offer professional help, community support, self-help tools, and more. What aspect of mental well-being are you looking to improve?"
    ]
        }

        # Get user input from the request
        user_message = request.data.get('message', '')

        if not user_message:
            return Response({"error": "No message provided."}, status=400)

        try:
            # Preprocess the user input and make predictions using ML model
            model, vectorizer = self.model
            if NLTK_DATA_AVAILABLE:
                stop_words = set(stopwords.words('english'))
            else:
                stop_words = set()

            tokens = word_tokenize(user_message.lower())
            filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
            user_input_vectorized = vectorizer.transform([' '.join(filtered_tokens)])

            # Predict the intent using the ML model
            predicted_intent_ml = model.predict(user_input_vectorized)[0]

            # Count word frequencies in the user's message
            word_freq = Counter(filtered_tokens)

            # Determine intent by matching most frequent words with intents
            intent_scores = {}
            for intent, phrases in self.intents.items():
                intent_score = 0
                for phrase in phrases:
                    phrase_tokens = word_tokenize(phrase.lower())
                    for token in phrase_tokens:
                        if token in word_freq:
                            intent_score += word_freq[token]
                intent_scores[intent] = intent_score

            # Select the intent with the highest score
            predicted_intent_freq = max(intent_scores, key=intent_scores.get)

            # Combine ML prediction and frequency-based prediction
            if intent_scores[predicted_intent_freq] > 0:
                predicted_intent = predicted_intent_freq
            else:
                predicted_intent = predicted_intent_ml

            # Randomly select a response based on the predicted intent
            response_message = random.choice(responses.get(predicted_intent, responses["unknown"]))

            return Response({"intent": predicted_intent, "response": response_message}, status=200)

        except Exception as e:
            return Response({"error": str(e)}, status=500)


        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info_dashboard(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        first_name = request.user.first_name
        last_name = request.user.last_name
        username = request.user.username

        user_info = {
            'user_id': user_id,
            'first_name': first_name,
            'last_name': last_name,
            'username': username,
        }
        print(user_id)
        return JsonResponse(user_info)
    else:
        return JsonResponse({'error': 'User is not authenticated'}, status=401)

def get_user_username(request):
    user = request.user
    user_info = {
        'username': user.username,
    }
    return JsonResponse(user_info)

@api_view(['GET'])
def get_user_data(request):
    user = request.user  # Get the currently authenticated user
    serializer = UserSerializer(user)  # Serialize the user data
    return Response(serializer.data)

@api_view(['POST'])
def logout_view(request):
    # Logout the user
    logout(request)
    # Return a success response
    return Response({'message': 'Logout successful'})



@api_view(['POST'])
def signup(request):
    first_name = request.data.get('firstName')
    last_name = request.data.get('lastName')
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if the user already exists
    if User.objects.filter(username=username).exists():
        return Response({'errors': {'username': ['User profile with this username already exists.']}}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(email=email).exists():
        return Response({'errors': {'email': ['User profile with this email already exists.']}}, status=status.HTTP_400_BAD_REQUEST)
    # Create the User
    user = User.objects.create(username=username, email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    user.save()

    return Response({'message': 'User signed up successfully.'}, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if a user with the provided email exists
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        print("Login failed. User with the provided email does not exist.")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    # Verify the password
    user = authenticate(request, username=email, password=password)

    if user:
        # Login successful
        login(request, user)
        print(f"Login successful for user: {user.username}")
        return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
    else:
        # Invalid credentials
        print("Login failed. Invalid username or password.")
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
def forgot_password(request):
    if request.method == 'POST':
        # Extract email from POST data
        email = request.POST.get('email', '')
        
        # Check if the email is associated with an existing user
        if User.objects.filter(email=email).exists():
            # Generate verification code
            verification_code = generate_verification_code()
            
            # Save verification code in the user's profile (you need to implement this)
            user = User.objects.get(email=email)
            user.profile.verification_code = verification_code
            user.profile.save()

            # Your email sending logic with verification code
            send_mail(
            'Verification Code',
            f'Your verification code is: {verification_code}',
            'team@serenimind.com.ng',  # Replace with your from email
            [email],
            fail_silently=False,
        )

            # Return a success response
            return JsonResponse({'success': True, 'message': 'Verification code sent successfully'})
        else:
            # Return an error response if the email is not found
            return JsonResponse({'success': False, 'message': 'Email not found in our records'})

    # Return a CSRF token in case of a GET request
    csrf_token = get_token(request)
    return JsonResponse({'csrfToken': csrf_token})

# Assuming this is part of your views.py
# Assuming this is part of your views.py
verification_codes = {}

def generate_verification_code(email):
    # Generate a random 6-digit code
    code = ''.join(random.choices(string.digits, k=6))

    # Store the verification code in the cache for later verification
    cache.set(email, code)

    # Print the verification code in the console for debugging
    print(f'Generated verification code for {email}: {code}')

    # Send verification code via email
    send_mail(
        'Verification Code',
        f'Your verification code is: {code}',
        'from@example.com',
        [email],
        fail_silently=False,
    )

    return code



@csrf_exempt
@api_view(['POST'])
def verification(request):
    email = request.data.get('email')
    verification_code = request.data.get('code')
    
    # Print statements for debugging
    print(f"Received verification code: {verification_code}")
    print(f'Stored verification code {verification_code} for email {email}')

    # Set the verification code in the cache
    cache.set(email, verification_code)
    print(f'Stored verification code {verification_code} for email {email}')

    # Retrieve the stored verification code
    stored_code = cache.get(email)
    print(f"Expected verification code: {stored_code}")

    # Check if the verification code is valid
    if verify_verification_code(email, verification_code):
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        return Response({'message': 'Verification successful'}, status=status.HTTP_200_OK)
    else:
        print("Verification failed!")
        return Response({'error': 'Invalid verification code'}, status=status.HTTP_400_BAD_REQUEST)


# Helper function to verify the verification code
def verify_verification_code(email, code):
    # Retrieve the stored code from the cache
    stored_code = cache.get(email)

    # Check if the stored code matches the received code
    return stored_code == code

@csrf_exempt
@api_view(['POST']) 
def password_reset(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            # Here you would generate a password reset token and send it to the user's email
            # For simplicity, let's assume we just send a static message for now
            send_mail(
                'Password Reset Request',
                'Please follow the link to reset your password.',
                'from@example.com',
                [email],
                fail_silently=False,
            )
            return JsonResponse({'message': 'Password reset email sent successfully.'})
        else:
            return JsonResponse({'message': 'User with this email does not exist.'}, status=400)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)
@csrf_exempt
@require_POST
def send_verification_email(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        verification_code = data.get('verificationCode')

        # Send verification email using Django's send_mail
        send_mail(
            'Verification Code',
            f'Your verification code is: {verification_code}',
            'team@serenimind.com.ng',  # Replace with your from email
            [email],
            fail_silently=False,
        )
        return JsonResponse({'message': 'Verification email sent successfully'}, status=200)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})


class CsrfTokenAPIView(APIView):
    def get(self, request, *args, **kwargs):
        csrf_token = get_token(request)
        return JsonResponse({'csrf_token': csrf_token})

@csrf_exempt
@csrf_exempt
def submit_form(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        date = data.get('date')
        time = data.get('time')
        reason = data.get('reason')
        phone_number = data.get('phoneNumber')
        email = data.get('email')
        language = data.get('language')
        plan = data.get('plan')
        anonymous = data.get('anonymous')

        # Send email to team@serenimind.com.ng
        timingotech_message = f'New booking details:\nDate: {date}\nTime: {time}\nReason: {reason}\nPhone Number: {phone_number}\nEmail: {email}\nLanguage: {language}\nPlan: {plan}\nAnonymous: {anonymous}'
        send_mail(
            'New Booking',
            timingotech_message,
            'team@serenimind.com.ng',  # Replace with your email
            ['team@serenimind.com.ng'],
            fail_silently=False,
        )

        # Send email to the user
        user_message = f'Thank you for booking a mental health professional. We will contact you via email or phone soon.\n\nBooking Details:\nDate: {date}\nTime: {time}\nReason: {reason}\nLanguage: {language}\nPlan: {plan}\nAnonymous: {anonymous}. \n\n Best regards,\n SereniMind.'
        send_mail(
            'Booking Confirmation',
            user_message,
            'team@serenimind.com.ng',  # Replace with your email
            [email],
            fail_silently=False,
        )

        return JsonResponse({'message': 'Form submitted successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)

@api_view(['GET'])
def get_user_profile(request, username):
    try:
        user_profile = UserProfile.objects.get(username=username)
        serializer = UserProfileSerializer(user_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
def update_user_profile(request, username):
    try:
        user_profile = UserProfile.objects.get(username=username)
        serializer = UserProfileSerializer(user_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except UserProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def post_list(request):
    posts = Post.objects.all().order_by('-timestamp')
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def post_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def create_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        fullname = request.POST.get('fullname')
        email = request.POST.get('email')

        # Save the blog post to the database
        blog_post = BlogPost.objects.create(
            title=title,
            content=content,
            image=image,
            fullname=fullname,
            email=email
        )

        # Construct email message
        email_subject = f'New Blog Post Created by {fullname}'
        email_message = f'Hello {fullname},\n\nThank you for creating a new blog post titled "{title}". Your blog is under review and would be sent in less than an hour.\n\nBest regards,\nSereniMind'
        timingotech_message = f' {fullname} Just sent a blog in using "{email}",\n\nThe content and image below, \n content:"{content}" \n image:"{image}" . \n\nBest regards,\nSereniMind'

        # Send email notification
        send_mail(
            email_subject,
            timingotech_message,
            'team@serenimind.com.ng',  # Replace with your email
            ['team@serenimind.com.ng'],
            fail_silently=False,
        )

        send_mail(
            email_subject,
            email_message,
            'team@serenimind.com.ng',  # Replace with your email
            [email],  # Send to the email provided by the user
            fail_silently=False,
        )

        return JsonResponse({'message': 'Blog post submitted successfully.'})
    else:
        return JsonResponse({'error': 'Only POST requests are allowed for this endpoint.'}, status=405)
    
@api_view(['GET', 'POST'])
def journal_entries(request):
    if request.method == 'GET':
        user = request.user
        print(user)
        if user.is_authenticated:
            entries = JournalEntry.objects.filter(user=user)
        else:
            entries = JournalEntry.objects.none()
        serializer = JournalEntrySerializer(entries, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        user = request.user
        print(user)
        if user.is_authenticated:
            serializer = JournalEntrySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'User authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['GET', 'PUT', 'DELETE'])
def journal_entry_detail(request, pk):
    try:
        entry = JournalEntry.objects.get(pk=pk)
    except JournalEntry.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = JournalEntrySerializer(entry)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = JournalEntrySerializer(entry, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        entry.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class MessageListCreateAPIView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    # You may need to override `perform_create` to associate user and community with the message


class MessageListCreate(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        community_id = self.kwargs['community_id']
        return Message.objects.filter(community_id=community_id)

class MessageRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer



class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer



class MessageDetailView(RetrieveUpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageEditView(RetrieveUpdateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

class MessageDeleteView(DestroyAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

#Login User

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class HomeView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)
    

class LogoutView(APIView):
     permission_classes = (IsAuthenticated,)
     def post(self, request):
          
          try:
               refresh_token = request.data["refresh_token"]
               token = RefreshToken(refresh_token)
               token.blacklist()
               return Response(status=status.HTTP_205_RESET_CONTENT)
          except Exception as e:
               return Response(status=status.HTTP_400_BAD_REQUEST)
          


class SenderIdAPIView(APIView):
    def get(self, request, *args, **kwargs):
        message_id = kwargs.get('message_id')
        try:
            message = Message.objects.get(pk=message_id)
            serializer = SenderIdSerializer(message)
            return Response(serializer.data)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found'}, status=status.HTTP_404_NOT_FOUND)
        


class UserSettingsView(APIView):
    def get_user_settings(self, user):
        user_settings, created = UserSettings.objects.get_or_create(user=user)
        return user_settings

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_settings = self.get_user_settings(request.user)
        serializer = UserSettingsSerializer(user_settings)
        return Response(serializer.data)

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)
        
        user_settings = self.get_user_settings(request.user)
        serializer = UserSettingsSerializer(user_settings, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def open_library_proxy(request):
    # Get the query parameters from the client request
    q = request.GET.get('q', '')
    limit = request.GET.get('limit', 20)

    # Make a request to the Open Library API
    api_url = f'https://openlibrary.org/search.json?q={q}&limit={limit}'
    response = requests.get(api_url)

    # Return the API response to the client as JSON
    return JsonResponse(response.json())

# ViewSet for Todo model
class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    # Override create method to automatically assign logged-in user to the todo
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# ViewSet for MoodEntry model
class MoodEntryViewSet(viewsets.ModelViewSet):
    queryset = MoodEntry.objects.all()
    serializer_class = MoodEntrySerializer
    permission_classes = [permissions.IsAuthenticated]  # Ensure only authenticated users can access

    # Override create method to automatically assign logged-in user to the mood entry
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # Custom action to filter mood entries by date range
    @action(detail=False, methods=['GET'])
    def filter_by_date(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        mood_entries = MoodEntry.objects.filter(user=self.request.user, date__range=[start_date, end_date])
        serializer = self.get_serializer(mood_entries, many=True)
        return Response(serializer.data)
    
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todos(request):
    if request.method == 'GET':
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        user = request.user
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Updated POST logic for creating a todo
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def todos_list_create(request):
    if request.method == 'GET':
        user = request.user
        todos = Todo.objects.filter(user=user)
        serializer = TodoSerializer(todos, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        user = request.user  # Get the authenticated user
        # Ensure that deadline is passed in the request
        data = request.data.copy()  # Create a mutable copy of request data
        data['user'] = user.id  # Assign the user ID to the data
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save(user=user)  # Explicitly set the user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@permission_classes([IsAuthenticated])
@api_view(['GET', 'PUT', 'DELETE'])
def todo_detail_update_delete(request, pk):
    try:
        todo = Todo.objects.get(pk=pk)
    except Todo.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TodoSerializer(todo)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def complete_todo(request, todo_id):
    todo = get_object_or_404(Todo, pk=todo_id)
    todo.completed = True
    todo.save()
    serializer = TodoSerializer(todo)
    return Response(serializer.data)


class MoodEntryListCreateAPIView(generics.ListCreateAPIView):
    queryset = MoodEntry.objects.all()
    serializer_class = MoodEntrySerializer

class MoodEntryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = MoodEntry.objects.all()
    serializer_class = MoodEntrySerializer



@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    # Get the user's username
    username = reset_password_token.user.username
    
    # Construct the email message with the username and ending with SereniMind Team
    email_plaintext_message = f"Hello {username},\n\nOpen the link to reset your password: {instance.request.build_absolute_uri('https://www.serenimind.com.ng/resetpasswordform/')}{reset_password_token.key}\n\nSereniMind Team"

    """
    Django's default send_mail function:
    Parameters: (title(email title), message(email body), from(email sender), to(recipient(s)))
    """
    send_mail(
        # title:
        f"Password Reset for {username}",
        # message:
        email_plaintext_message,
        # from:
        "team@serenimind.com.ng",
        # to:
        [reset_password_token.user.email],
        fail_silently=False,
    )


class DeleteUserAccountView(APIView):
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
@csrf_exempt
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


def custom_csrf_failure_view(request, reason=""):
    return HttpResponseForbidden("CSRF verification failed. Please try again.")

@csrf_exempt
def send_email(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('user_name')
        email = data.get('user_email')
        message = data.get('message')
        
        # Create a comprehensive message
        comprehensive_message = f"Message from {name} ({email}):\n\n{message}"
        
        # Send email to the receiver
        send_mail(
            f'New message from {name}',
            comprehensive_message,
            email,
            ['team@serenimind.com.ng'],  # replace with your email
            fail_silently=False,
        )
        return JsonResponse({'message': 'Email sent successfully'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def subscribe_newsletter(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('user_email')
        
        # Send email to the receiver
        send_mail(
            'New Newsletter Subscription',
            f'You have a new subscriber: {email}',
            'team@serenimind.com.ng',  # replace with your email
            ['team@serenimind.com.ng'],  # replace with your email
            fail_silently=False,
        )
        
        # Create a comprehensive subscription confirmation message
        comprehensive_subscription_message = f"""Dear Subscriber,\n\nThank you for subscribing to the SereniMind newsletter! We are thrilled to have you as part of our community. By subscribing, you are joining a dedicated group of individuals who are committed to enhancing their mental well-being and staying informed about the latest developments in mental health support.\n\nOur newsletter is crafted to bring you valuable insights, tips, and updates. You can look forward to receiving:\n\n- Exclusive articles and resources on mental health and wellness\n- Updates on new features and services offered by SereniMind\n- Inspirational stories and testimonials from our community\n- Information on upcoming events and webinars\n- Special promotions and offers\n\nAt SereniMind, we believe in the power of community and the importance of staying connected. Your journey towards better mental health is important to us, and we are here to support you every step of the way.\n\nIf you have any questions, feedback, or topics you would like us to cover, please do not hesitate to reach out. We are always here to help and listen.\n\nThank you once again for subscribing to our newsletter. We look forward to sharing valuable content with you and supporting you on your journey towards mental well-being.\n\nWarm regards,\nThe SereniMind Team
        """

        # Send email to the new subscriber
        send_mail(
            'Newsletter Subscription Confirmation',
            comprehensive_subscription_message,
            'team@serenimind.com.ng',  # replace with your email
            [email],
            fail_silently=False,
        )
        
        return JsonResponse({'message': 'Successfully subscribed to the newsletter'})
    return JsonResponse({'error': 'Invalid request'}, status=400)

class MoodAssessmentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = MoodAssessmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def report_message(request, message_id):
    try:
        message = Message.objects.get(id=message_id)
    except Message.DoesNotExist:
        return Response({"error": "Message not found"}, status=status.HTTP_404_NOT_FOUND)

    reporter = request.user
    
    # Create a new report
    report = Report.objects.create(
        message=message,
        reported_by=reporter
    )

    # Prepare email content
    subject = f"Message Reported in Community: {message.community.name}"
    email_body = f"""
    A message has been reported:

    Message ID: {message.id}
    Message Content: {message.content}
    Posted by: {message.user.username}
    Posted on: {message.timestamp}
    
    Reported by: {reporter.username}
    Report timestamp: {report.timestamp}

    Please review this message for any violations of community guidelines.
    """
    
    # Send email
    try:
        send_mail(
            subject,
            email_body,
            'team@serenimind.com.ng',  # replace with your email
            ['team@serenimind.com.ng'],
            fail_silently=False,
        )
    except Exception as e:
        # Log the error, but don't expose it to the user
        print(f"Error sending email: {str(e)}")

    return Response({"message": "Report submitted successfully"}, status=status.HTTP_201_CREATED)
