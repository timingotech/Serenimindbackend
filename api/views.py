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
import os
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import random  # Import random for selecting responses

# Download required NLTK data
# Ensure NLTK data is downloaded
NLTK_DATA_PATH = '/opt/render/punkt'
if not os.path.exists(NLTK_DATA_PATH):
    os.makedirs(NLTK_DATA_PATH)

nltk.data.path.append(NLTK_DATA_PATH)

try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('tokenizers/punkt_tab')
    nltk.data.find('corpora/stopwords')
    NLTK_DATA_AVAILABLE = True
except LookupError:
    nltk.download('punkt', download_dir=NLTK_DATA_PATH)
    nltk.download('punkt_tab', download_dir=NLTK_DATA_PATH)
    nltk.download('stopwords', download_dir=NLTK_DATA_PATH)
    NLTK_DATA_AVAILABLE = True

class ChatbotView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_or_train_model()

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
        # Updated intent training data
        intents = {
            "greet": ["hello", "hi", "greetings", "good morning"],
            "goodbye": ["bye", "goodbye", "see you later"],
            "thanks": ["thanks", "thank you"],
            "help": ["help", "can you assist", "need support"],
            # New intents
            "weather": ["what's the weather", "weather update", "tell me the weather"],
            "joke": ["tell me a joke", "make me laugh", "say something funny"],
            "mood": ["I'm feeling sad", "I'm happy", "I'm stressed out", "I'm anxious"],
        }

        # Tokenization and stopword removal using NLTK
        if NLTK_DATA_AVAILABLE:
            stop_words = set(stopwords.words('english'))
        else:
            stop_words = set()  # In case NLTK data isn't available

        all_texts = []
        all_labels = []
        for intent, phrases in intents.items():
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
            "greet": [
                "Hello! How can I assist you today?",
                "Hi there! What can I help you with?",
                "Greetings! How may I help you?"
            ],
            "goodbye": [
                "Goodbye! Take care.",
                "See you later! Have a great day!",
                "Farewell! Until next time!"
            ],
            "thanks": [
                "You're welcome! Happy to help.",
                "No problem! I'm here if you need anything else.",
                "Glad I could assist!"
            ],
            "help": [
                "Sure! Let me know what you need assistance with.",
                "I'm here to help! What do you need?",
                "How can I assist you today?"
            ],
            # New responses
            "weather": [
                "The weather is sunny with a slight breeze. Is there anything else you need?",
                "It's raining outside. Don't forget your umbrella!",
                "Expect a cold front later today. Stay warm!"
            ],
            "joke": [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my computer I needed a break, and now it won't stop sending me ads for vacations!",
                "Why did the scarecrow win an award? Because he was outstanding in his field!"
            ],
            "mood": [
                "I'm here for you. Would you like some tips on managing stress or improving your mood?",
                "It's okay to feel that way. Talking helps, do you want to chat more?",
                "Remember, it’s okay to express how you feel. How can I support you?"
            ],
            "unknown": [
                "I'm not sure I understand. Could you rephrase?",
                "Could you clarify what you mean?",
                "I'm sorry, I didn't get that. Can you say it differently?"
            ]
        }

        # Get user input from the request
        user_message = request.data.get('message', '')

        if not user_message:
            return Response({"error": "No message provided."}, status=400)

        # Preprocess the user input and make predictions
        try:
            model, vectorizer = self.model
            if NLTK_DATA_AVAILABLE:
                stop_words = set(stopwords.words('english'))
            else:
                stop_words = set()

            tokens = word_tokenize(user_message.lower())
            filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
            user_input_vectorized = vectorizer.transform([' '.join(filtered_tokens)])

            # Predict the intent
            predicted_intent = model.predict(user_input_vectorized)[0]

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
