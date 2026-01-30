from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail 
from django.http import HttpResponseForbidden 
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User 
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
from django.http import JsonResponse 
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
from django.http import HttpResponseForbidden
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from rest_framework import generics 
from django.dispatch import receiver 
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail 
from .serializers import CommunitySerializer
from django.core.cache import cache
from django.contrib.auth.models import User
from django.http import JsonResponse 
import os
from rest_framework.generics import RetrieveUpdateAPIView, DestroyAPIView
from .models import Message
from .serializers import MessageSerializer
from .models import Message
from .serializers import MessageSerializer, MyTokenObtainPairSerializer
from django.contrib.auth.models import User 
from django.contrib.auth.models import User 
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.models import User 
from rest_framework.response import Response
from rest_framework import status 
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
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated 
from rest_framework.views import APIView
from rest_framework.response import Response 
import os
import pickle 
import json 
from sklearn.feature_extraction.text import TfidfVectorizer 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords 
import nltk
import random
from collections import Counter 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from sklearn.linear_model import LogisticRegression
from django.db import models
from datetime import datetime
import json
from .models import BotSettings
from .serializers import BotSettingsSerializer
import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
import os
from .models import UserConversation
from .models import ActivityMovie, ActivityGame, ActivityExercise, ActivitySound
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ContactSerializer
from .serializers import ActivityMovieSerializer, ActivityGameSerializer, ActivityExerciseSerializer, ActivitySoundSerializer
from .serializers import BlogPostSerializer
from django.core.mail import EmailMessage

# Download required NLTK data
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
    permission_classes = [IsAuthenticated]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.load_or_train_model()
        self.intents = {
        "greeting": [
    "hello", "hi", "hey", "good morning", "good afternoon", "good evening", "hi there", "hello there", "how are you doing", "how are you",
    "greetings", "how are you","how are you doing", "nice to meet you", "pleasure to meet you", "good day", "morning", 
    "evening", "howdy", "hey there", "hiya", "what's up", "sup", "yo", "welcome", "yo", "sup", "wassup", "wazzup", "whassup", "what up", "howdy", "hey yo", "yo yo",
    "how far", "how far na", "wetin dey", "wosop", "wasop", "wossop", "wazaa", "wazzaa",
    "hai", "hei", "heey", "heyy", "heyyy", "hiiii", "hiii", "hii", "henlo", "hewwo",
    "ello", "elo", "eyy", "ayy", "ayyy", "ayyyy", "aye", "ay", "heyo", "hellooo",
    "heluu", "helu", "halla", "hola", "ohai", "ohayo", "oi", "oy", "yooo", "yoo",
    "what's good", "whatsgood", "wuts good", "wusgood", "wassgood", "whats gud",
    "what's crackin", "whatcha up to", "whatchu up to", "wyd", "wyd?", "sup wit u",
    "what's popping", "what's poppin", "wuts poppin", "wassup wit u", "how u",
    "what's the word", "word up", "what it do", "what it is", "what's the deal",
    "what's the business", "what's the move", "what's the scene", "what's the vibe",
    "what's the story", "what's the latest", "what's cooking", "what's brewing",
    "wagwan", "wag1", "wasgood", "wassgud", "wass gud", "wass good", "waga", 
    "what gwaan", "whagwan", "wagwaan", "weh yuh deh pon", "yuh good",
    "g'day", "hiya", "heya", "hy", "hi", "hey", "lo", "hlo", "hullo", "ello m8",
    "hey m8", "hi m8", "sup m8", "yo m8", "oi m8", "ey", "eyyy", "eh",
    "what's cooking good looking", "hey stranger", "hey buddy", "hey bud", "hey pal",
    "hey homie", "hey fam", "hey bruh", "hey bruv", "hey bro", "hey sis", "hey girl",
    "hey dude", "hey mate", "hey chief", "hey boss", "hey fella", "hey hun",
    "hmu", "slide thru", "pull up", "check in", "check it", "ping me", "hit me up",
    "drop in", "roll thru", "pop in", "link up", "pull thru", "reach",
    "howdy doody", "hihi", "heyhey", "yoyo", "helloooo", "hiyaa", "heyaa",
    "herro", "harro", "wassuuup", "wassaaaap", "whaddup", "whaddap", "whatitdo",
    "yo like", "hey like", "sup like", "ey yo", "ay yo", "eh yo", "aye yo",
    "yo fam", "hey fam", "sup fam", "ey fam", "ay fam", "eh fam", "aye fam",
    "henlo frend", "hewwo", "hai there", "herrow", "haiii", "haii", "ohaii",
    "ohai there", "haay", "haaay", "haaaay", "heeeey", "yoohoo", "yahoo",
    "helo", "helllo", "hallo", "hullo", "heylo", "heloo", "hellooo", "helou",
    "helu", "heyu", "heyo", "hiya", "hiyo", "hihi", "hiii", "hiiiii",
    "wasabi", "que pasa", "que tal", "que onda", "konichiwa", "ohayo", "annyeong",
    "nihao", "ciao", "aloha", "bonjour", "hola", "namaste", "salaam",
    "what's crackalackin", "what's poppin", "what's cracking", "what's jumping",
    "what's shaking", "what's cooking", "what's happening", "what's new",
    "glhf", "o/", "hey all", "hi all", "greets", "hai all", "hoi", "hoiii",
    "heyo all", "hey peeps", "hi peeps", "greetings peeps", "yello", "yellow",
    "how you living", "how you doing", "how u doin", "how r u", "how r ya",
    "how ya doin", "howre you", "how're ya", "how u livin", "how u living",
    "peek a boo", "knock knock", "guess who", "look who's here", "surprise",
    "boom", "bam", "pow", "zing", "zoom", "whoosh", "tadaa", "ta-da",
    "uwu", "owo", "^_^", ":3", "^-^", "^.^", ":D", "xD", "XD", ":P",
    "sksksk", "periodt", "period", "purr", "bestie", "besties", "bestieee",
    "girlie", "girlyyy", "queeen", "slayyy", "yas", "yaaas", "yassss",
    "tbh", "ngl", "fr", "frfr", "ong", "istg", "iykyk", "fax", "no cap",
    "cap", "bet", "say less", "word", "facts", "fr tho", "ong tho",
    "yeet", "sheesh", "sheeesh", "oop", "oop-", "bruh", "bruhhh", "brooo",
    "duuude", "dudee", "mateee", "famm", "fammm", "homieee", "yurrr", "yurr",
    "morning sunshine", "rise and shine", "top of the morning", "early morning greetings", 
    "dawn greetings", "sunrise hello", "morning blessings", "blessed morning", "bright morning",
    "fresh morning", "beautiful morning", "wonderful morning", "happy morning", "joyous morning",
    "peaceful morning", "lovely morning", "pleasant morning", "glorious morning", "splendid morning",
    "magnificent morning", "marvelous morning", "delightful morning", "cheerful morning",
    "good morning sunshine", "morning joy", "morning bliss", "morning cheer", "morning light",
    "morning glory", "morning star", "morning blessing", "morning wishes", "morning greetings",
    "afternoon delight", "good day to you", "pleasant afternoon", "wonderful afternoon",
    "beautiful afternoon", "lovely afternoon", "peaceful afternoon", "joyous afternoon",
    "splendid afternoon", "magnificent afternoon", "marvelous afternoon", "delightful afternoon",
    "cheerful afternoon", "afternoon joy", "afternoon bliss", "afternoon cheer", "afternoon light",
    "afternoon blessing", "afternoon wishes", "afternoon greetings", "midday greetings",
    "sunny afternoon", "bright afternoon", "warm afternoon", "gentle afternoon",
    "evening blessings", "pleasant evening", "wonderful evening", "beautiful evening",
    "peaceful evening", "joyous evening", "splendid evening", "magnificent evening",
    "marvelous evening", "delightful evening", "cheerful evening", "evening joy",
    "evening bliss", "evening cheer", "evening light", "evening star", "evening blessing",
    "evening wishes", "evening greetings", "starry evening", "moonlit evening", "twilight greetings",
    "dusk greetings", "sunset hello", "nightfall greetings", "midnight greetings",
    "greetings and salutations", "pleased to make your acquaintance", "how do you do",
    "it's a pleasure", "delighted to meet you", "welcome to you", "good day to you sir",
    "good day to you madam", "esteemed greetings", "cordial greetings", "formal salutations",
    "proper greetings", "distinguished greetings", "respectful greetings", "honored to meet you",
    "pleasure to meet your acquaintance", "at your service", "good day to you all",
    "greetings to you", "salutations to all", "formal welcome", "proper welcome",
    "distinguished welcome", "respectful welcome", "honored welcome",
    "hey buddy", "what's happening", "what's new", "how goes it", "how's it hanging",
    "how's tricks", "what's cooking", "what's the word", "what's good", "what's up doc",
    "howdy partner", "how ya doing", "how you doing", "how's life", "how's everything",
    "wassup", "sup buddy", "yo yo", "heya", "hiya pal", "hi friend", "hey friend",
    "hey there friend", "hi there pal", "hey there buddy", "what's the story",
    "what's cracking", "what's popping", "what's cooking good looking",
    "welcome aboard", "welcome back", "welcome home", "glad to have you", "nice to have you here",
    "great to see you", "good to have you", "pleased to have you", "delighted to have you",
    "wonderful to have you", "welcome to the family", "welcome to the team", "welcome to the group",
    "welcome to the community", "welcome to our home", "welcome to our place", "welcome in",
    "please come in", "do come in", "make yourself at home", "welcome welcome",
    "bonjour", "hola", "ciao", "namaste", "aloha", "guten tag", "konnichiwa", "shalom",
    "salaam", "ni hao", "annyeong", "sawadee", "merhaba", "zdravstvuyte", "buenos dias",
    "bom dia", "god dag", "dobry den", "kalimera", "selamat pagi", "xin chao", "vanakkam",
    "namaskar", "assalamu alaikum", "salam", "dia dhuit", "tere", "hej", "hallo", "privet",
    "lovely to see you", "wonderful to see you", "delighted to see you", "pleased to see you",
    "happy to see you", "glad to see you again", "great to see you again", "nice to see you again",
    "wonderful to see you again", "delighted to see you again", "pleased to see you again",
    "happy to see you again", "good to see you again", "lovely to see you again",
    "marvelous to see you again", "splendid to see you again", "fantastic to see you again",
    "how have you been", "how's your day", "how's your day going", "how's your morning",
    "how's your afternoon", "how's your evening", "how's everything going", "how are things",
    "how's life treating you", "how have things been", "how's it all going", "how are you doing",
    "how are you feeling", "how's your world", "how's your week been", "how's your day been",
    "how are you today", "how are you this morning", "how are you this afternoon",
    "how are you this evening", "how's your life", "how's your family", "how's work",
    "how's your health", "how's your mood",
    "hello!", "hi!", "hey!", "greetings!", "welcome!", "good morning!", "good afternoon!",
    "good evening!", "howdy!", "hiya!", "heya!", "what's up!", "yo!", "hey there!",
    "hi there!", "hello there!", "greetings and salutations!", "welcome aboard!",
    "welcome back!", "welcome home!", "great to see you!", "lovely to see you!",
    "wonderful to see you!", "delighted to see you!", "pleased to see you!",
    "g'day", "ey up", "hiya love", "how you going", "how ya going", "kia ora", "guid mornin",
    "top o' the morning", "howdy y'all", "hey youse", "hey you lot", "alright mate",
    "right mate", "hiya mate", "hey mate", "g'day mate", "oi mate", "hey folks",
    "hi everyone", "hello everybody", "greetings everyone", "hey everyone", "hi everybody",
    "back again", "returned", "i'm back", "hello again", "hi again", "hey again",
    "good morning again", "good afternoon again", "good evening again", "here again",
    "returned again", "back once more", "here once more", "hello once more",
    "hi once more", "hey once more", "greetings once more", "welcome back again",
    "blessed morning to you", "wonderful day to you", "beautiful evening to you",
    "peaceful morning to you", "joyous day to you", "bright morning to you",
    "sunny day to you", "starry evening to you", "lovely morning to you",
    "pleasant day to you", "delightful evening to you", "cheerful morning to you",
    "happy day to you", "blessed evening to you", "wonderful morning to you",
    "beautiful day to you", "peaceful evening to you", "joyous morning to you",
    "hope you're doing well", "hope you're well", "hope all is well", "trust you're well",
    "trust all is well", "hope you're having a good day", "hope you're having a great day",
    "hope you're having a wonderful day", "hope you're having a beautiful day",
    "hope you're having a blessed day", "hope you're having a peaceful day",
    "hope you're having a joyous day", "hope you're having a bright day",
    "hope you're having a lovely day", "hope you're having a pleasant day",
    "nice day isn't it", "beautiful day isn't it", "lovely weather we're having",
    "great day for it", "perfect day for it", "wonderful weather we're having",
    "nice weather we're having", "beautiful weather isn't it", "lovely day for it",
    "perfect weather isn't it", "great weather we're having", "wonderful day isn't it",
    "spring greetings", "summer greetings", "autumn greetings", "winter greetings",
    "seasonal greetings", "spring hello", "summer hello", "autumn hello", "winter hello",
    "springtime greetings", "summertime greetings", "autumn wishes", "winter wishes",
    "spring wishes", "summer wishes",
    "sunny greetings", "rainy day greetings", "snowy greetings", "cloudy day hello",
    "stormy weather greetings", "foggy morning hello", "misty morning greetings",
    "warm weather hello", "cold weather greetings", "windy day hello", "frosty morning greetings",
    "hot day greetings", "chilly morning hello",
    "greetings colleagues", "morning team", "hello everyone", "good morning all",
    "greetings all", "welcome everyone", "hello team", "morning everyone",
    "good morning team", "greetings team", "welcome team", "hello colleagues",
    "morning colleagues", "good morning colleagues", "greetings staff",
    "namaste ji", "as-salaam-alaikum", "shalom aleichem", "konbanwa", "ohayou gozaimasu",
    "annyeong haseyo", "ni hao ma", "xin chao ban", "sawadee krap", "sawadee ka",
    "buenos tardes", "buenos noches", "bonsoir", "buongiorno", "buonasera",
    "fair morning to you", "fair day to you", "fair evening to you", "good morrow",
    "well met", "hail and well met", "hail friend", "well met friend", "good morrow to you",
    "fair greetings", "gentle greetings", "kind greetings", "fair tidings",
    "hey fam", "sup fam", "hey squad", "hi squad", "hey crew", "hi crew",
    "squad up", "crew check", "fam check", "gang's all here", "hey everyone",
    "squad goals", "crew love", "fam first", "hey peeps", "hi peeps",
    "greetings of the day", "time of day greetings", "daily greetings",
    "friendly greetings", "warm greetings", "kind greetings", "gentle greetings",
    "cheerful greetings", "happy greetings", "joyful greetings", "peaceful greetings",
    "blessed greetings", "wonderful greetings", "beautiful greetings", "lovely greetings",
    "pleasant greetings", "delightful greetings", "marvelous greetings",
    "splendid greetings", "magnificent greetings", "glorious greetings"
  ],
    "farewell": [
        "goodbye", "bye", "talk later", "need to go",
        "thanks for chat", "until next time", "good night",
        "take care", "see you", "bye for now"
    ],
    "General_Anxiety_Assessment": [
        "how anxious am i", "evaluate my anxiety", "is this anxiety normal",
        "anxiety level check", "do i have anxiety", "anxiety self assessment",
        "rate my anxiety symptoms", "anxiety severity check", "analyze my anxiety",
        "anxiety evaluation request", "check anxiety levels", "anxiety test needed",
        "assess my mental state", "anxiety diagnosis help", "measure anxiety severity",
        "anxiety screening request", "evaluate stress levels", "anxiety check please",
        "understand my anxiety", "anxiety assessment needed", "anxiety quiz request",
        "gauge my anxiety", "anxiety level measurement", "analyze stress symptoms",
        "check if i have anxiety", "anxiety scale assessment", "review my symptoms",
        "anxiety evaluation needed", "mental health check", "anxiety analysis request",
        "validate my anxiety", "anxiety level test", "am i experiencing anxiety",
        "assess panic symptoms", "anxiety disorder check", "evaluate mental state",
        "anxiety score needed", "check anxiety severity", "anxiety assessment tools",
        "anxiety level monitor", "review anxiety patterns", "anxiety check up",
        "anxiety self evaluation", "mental wellness check", "anxiety level analysis",
        "assess anxiety condition", "anxiety rating request", "evaluate symptoms",
        "anxiety screening test", "check anxiety status", "anxiety measurement help",
        "anxiety level indicator", "assess mental health", "anxiety evaluation report",
        "anxiety symptoms check", "anxiety assessment form", "gauge stress levels",
        "anxiety level reading", "mental state analysis", "anxiety evaluation help",
        "assess anxiety type", "anxiety pattern check", "evaluate anxiety state",
        "anxiety level gauge", "anxiety screening help", "mental health assessment",
        "anxiety condition check", "evaluate anxiety impact", "anxiety severity test",
        "anxiety level review", "mental wellness assessment", "anxiety check report",
        "assess anxiety impact", "anxiety rating scale", "evaluate anxiety symptoms",
        "anxiety level status", "anxiety screening results", "mental health review",
        "anxiety condition test", "evaluate anxiety levels", "anxiety severity check",
        "anxiety level evaluation", "mental state check", "anxiety test results",
        "assess anxiety severity", "anxiety rating check", "evaluate anxiety state",
        "anxiety level analysis", "anxiety screening status", "mental health gauge",
        "anxiety condition review", "evaluate anxiety patterns", "anxiety test help",
        "anxiety level report", "mental state evaluation", "anxiety check status",
        "assess anxiety patterns", "anxiety rating review", "evaluate anxiety type",
        "anxiety level status", "anxiety screening check", "mental health monitor",
        "anxiety condition gauge", "evaluate anxiety severity", "anxiety test update",
        "anxiety level check up", "mental state assessment", "anxiety review needed",
        "assess anxiety state", "anxiety rating status", "evaluate anxiety impact",
        "anxiety level monitor", "anxiety screening review", "mental health status",
        "anxiety condition status", "evaluate anxiety condition", "anxiety test check"
    ],
    "Triggers_and_Causes": [
        "what triggers my anxiety", "anxiety cause identification", "why am i anxious",
        "anxiety trigger patterns", "common anxiety causes", "identify anxiety triggers",
        "what makes me anxious", "anxiety source analysis", "trigger recognition help",
        "anxiety cause assessment", "find anxiety triggers", "why do i feel anxious",
        "anxiety trigger tracking", "understanding anxiety causes", "identify stress triggers",
        "anxiety source check", "what starts my anxiety", "trigger identification help",
        "anxiety cause tracking", "recognize anxiety patterns", "what triggers panic",
        "anxiety factor analysis", "understand my triggers", "cause identification help",
        "anxiety trigger list", "what causes my stress", "trigger pattern recognition",
        "anxiety source tracking", "identify panic triggers", "what makes anxiety worse",
        "anxiety cause patterns", "understand trigger factors", "anxiety origin help",
        "trigger source check", "what causes anxiety attacks", "anxiety factor tracking",
        "identify stress sources", "what triggers panic attacks", "anxiety cause recognition",
        "understand my stressors", "trigger analysis help", "anxiety source patterns",
        "identify anxiety sources", "what causes my panic", "anxiety trigger assessment",
        "understand stress factors", "cause tracking help", "anxiety pattern recognition",
        "identify trigger patterns", "what makes me panic", "anxiety source identification",
        "understand anxiety factors", "trigger evaluation help", "anxiety cause tracking",
        "identify anxiety patterns", "what causes my attacks", "anxiety trigger recognition",
        "understand panic sources", "cause analysis help", "anxiety factor patterns",
        "identify stress patterns", "what triggers my attacks", "anxiety source evaluation",
        "understand trigger sources", "cause identification support", "anxiety pattern tracking",
        "identify panic sources", "what makes me stressed", "anxiety trigger analysis",
        "understand stress sources", "cause recognition help", "anxiety factor tracking",
        "identify trigger sources", "what causes my stress", "anxiety source recognition",
        "understand anxiety sources", "trigger pattern help", "anxiety cause analysis",
        "identify stress triggers", "what makes me anxious", "anxiety trigger evaluation",
        "understand panic triggers", "cause tracking support", "anxiety factor recognition",
        "identify anxiety factors", "what triggers my stress", "anxiety source patterns",
        "understand trigger patterns", "cause analysis support", "anxiety pattern analysis",
        "identify panic patterns", "what causes my anxiety", "anxiety trigger tracking",
        "understand stress patterns", "trigger recognition support", "anxiety factor evaluation",
        "identify trigger patterns", "what makes me panic", "anxiety source analysis",
        "understand anxiety patterns", "cause pattern help", "anxiety trigger recognition",
        "identify stress factors", "what triggers my panic", "anxiety cause patterns",
        "understand trigger factors", "pattern analysis help", "anxiety factor tracking",
        "identify panic factors", "what causes my attacks", "anxiety source evaluation",
        "understand stress factors", "trigger tracking support", "anxiety pattern recognition"
    ],
    "Physical_Symptoms": [
        "physical anxiety symptoms", "body anxiety signs", "anxiety physical effects",
        "anxiety body symptoms", "physical stress signs", "anxiety manifestations",
        "bodily anxiety symptoms", "physical anxiety signs", "anxiety body effects",
        "physical stress symptoms", "anxiety physical signs", "body stress effects",
        "physical manifestations", "anxiety body reactions", "physical stress signs",
        "anxiety physical impact", "body reaction symptoms", "physical anxiety effects",
        "anxiety somatic signs", "physical stress impact", "body anxiety reactions",
        "physical symptom check", "anxiety body signs", "physical stress effects",
        "anxiety physical signs", "body manifestations", "physical anxiety reactions",
        "anxiety somatic symptoms", "physical stress signs", "body anxiety effects",
        "physical reaction check", "anxiety body symptoms", "physical stress symptoms",
        "anxiety physical reactions", "body stress signs", "physical anxiety signs",
        "anxiety manifestation check", "physical symptoms list", "anxiety body effects",
        "physical stress reactions", "anxiety somatic signs", "body anxiety symptoms",
        "physical reaction tracking", "anxiety physical signs", "body stress effects",
        "physical symptom monitor", "anxiety manifestations", "physical anxiety symptoms",
        "body reaction check", "anxiety somatic effects", "physical stress signs",
        "anxiety body reactions", "physical symptom analysis", "anxiety physical effects",
        "body manifestation check", "anxiety stress symptoms", "physical reaction signs",
        "anxiety body signs", "physical symptom tracking", "anxiety manifestation effects",
        "body reaction monitor", "anxiety physical symptoms", "physical stress reactions",
        "anxiety somatic signs", "body symptom check", "physical anxiety effects",
        "anxiety manifestation signs", "body reaction tracking", "physical stress symptoms",
        "anxiety physical reactions", "body symptom monitor", "anxiety somatic effects",
        "physical manifestation check", "anxiety body symptoms", "physical reaction signs",
        "anxiety stress effects", "body symptom tracking", "physical anxiety reactions",
        "anxiety manifestation monitor", "physical stress signs", "body reaction effects",
        "anxiety somatic symptoms", "physical symptom check", "anxiety body reactions",
        "physical manifestation tracking", "anxiety stress signs", "body symptom effects",
        "anxiety physical signs", "physical reaction monitor", "anxiety manifestation symptoms",
        "body stress reactions", "physical symptom effects", "anxiety somatic signs",
        "physical manifestation monitor", "anxiety body effects", "physical reaction tracking",
        "anxiety stress symptoms", "body symptom signs", "physical anxiety manifestations",
        "anxiety somatic reactions", "physical symptom signs", "anxiety body signs",
        "physical manifestation effects", "anxiety stress reactions", "body symptom check",
        "physical anxiety signs", "anxiety somatic effects", "physical reaction symptoms",
        "anxiety manifestation signs", "body stress effects", "physical symptom reactions"
    ], 
    "Cognitive_Symptoms": [
        "racing thoughts anxiety", "anxious thinking patterns", "overthinking problems",
        "cant stop worrying", "anxiety thought loops", "mind wont quiet down",
        "constant worry thoughts", "anxiety mental symptoms", "scattered thinking anxiety",
        "negative thought patterns", "anxiety brain fog", "worried about everything",
        "mental anxiety signs", "catastrophic thinking", "cant focus anxiety",
        "anxiety thought patterns", "worrying too much", "mind racing anxiety",
        "obsessive thoughts anxiety", "cant concentrate anxiety", "anxiety mental state",
        "constant fear thoughts", "anxiety thinking problems", "mental clarity issues",
        "anxious mind symptoms", "thought spiral anxiety", "worry cycle help",
        "anxiety brain symptoms", "thinking problems anxiety", "mental focus issues",
        "anxiety concentration", "worried thinking patterns", "mind block anxiety",
        "thought process issues", "anxiety mental focus", "cognitive anxiety signs",
        "racing mind problems", "anxiety thought blocking", "mental stress symptoms",
        "constant anxiety thoughts", "cognitive thought patterns", "mind racing issues",
        "anxiety brain function", "worried mental state", "thought processing anxiety",
        "mental anxiety patterns", "cognitive stress signs", "racing thoughts help",
        "anxiety thinking issues", "worried thought cycles", "mind anxiety symptoms",
        "cognitive function anxiety", "mental processing issues", "anxiety thought help",
        "worried brain symptoms", "mind block issues", "anxiety cognitive signs",
        "mental clarity anxiety", "thought pattern help", "racing mind anxiety",
        "cognitive anxiety help", "worried thinking issues", "mind processing anxiety",
        "anxiety mental symptoms", "thought blocking help", "racing thoughts patterns",
        "cognitive issues anxiety", "worried brain function", "mind clarity anxiety",
        "anxiety processing issues", "thought anxiety help", "racing mind symptoms",
        "cognitive anxiety patterns", "worried mental function", "mind block symptoms",
        "anxiety thinking help", "thought processing issues", "racing brain patterns",
        "cognitive thought issues", "worried processing help", "mind anxiety patterns",
        "anxiety mental function", "thought clarity issues", "racing thoughts help",
        "cognitive processing anxiety", "worried thought patterns", "mind racing help",
        "anxiety brain patterns", "thought blocking anxiety", "racing mind issues",
        "cognitive anxiety symptoms", "worried thinking help", "mind processing issues",
        "anxiety mental patterns", "thought anxiety patterns", "racing brain help",
        "cognitive thought help", "worried brain patterns", "mind clarity issues",
        "anxiety processing help", "thought racing anxiety", "mental anxiety help",
        "cognitive function issues", "worried processing patterns", "mind block help",
        "anxiety thinking patterns", "thought clarity anxiety", "racing thoughts issues",
        "cognitive processing help", "worried mental patterns", "mind racing patterns"
    ],
    "Behavioral_Responses": [
        "avoiding situations anxiety", "anxiety coping behaviors", "nervous habits anxiety",
        "anxiety avoidance patterns", "stress reaction behaviors", "anxiety responses help",
        "panic behavior patterns", "anxiety reaction types", "stress response habits",
        "anxious behavior help", "panic response patterns", "anxiety habits check",
        "stress behavior types", "anxiety response analysis", "panic habits review",
        "avoiding people anxiety", "stress reaction patterns", "anxiety behavior check",
        "panic response types", "anxiety habits analysis", "stress behavior review",
        "anxious avoidance help", "panic reaction patterns", "anxiety response check",
        "stress habits analysis", "anxiety behavior review", "panic avoidance patterns",
        "stress response types", "anxiety habits check", "panic behavior analysis",
        "anxious reaction help", "stress avoidance patterns", "anxiety response review",
        "panic habits check", "anxiety behavior analysis", "stress reaction types",
        "anxious avoidance patterns", "panic response review", "anxiety habits help",
        "stress behavior patterns", "anxiety reaction analysis", "panic avoidance check",
        "stress response review", "anxiety behavior help", "panic reaction types",
        "anxious habits patterns", "stress avoidance analysis", "anxiety response types",
        "panic behavior review", "stress reaction check", "anxiety avoidance help",
        "panic habits patterns", "anxious response analysis", "stress behavior help",
        "anxiety reaction review", "panic avoidance types", "stress response patterns",
        "anxious behavior types", "panic reaction analysis", "anxiety habits review",
        "stress avoidance check", "anxiety response help", "panic behavior help",
        "anxious reaction patterns", "stress habits types", "anxiety avoidance analysis",
        "panic response help", "stress behavior types", "anxiety reaction check",
        "anxious habits help", "panic avoidance review", "stress response analysis",
        "anxiety behavior patterns", "panic reaction help", "anxious response types",
        "stress habits patterns", "anxiety avoidance review", "panic behavior types",
        "stress reaction analysis", "anxiety habits help", "anxious avoidance check",
        "panic response patterns", "stress behavior review", "anxiety reaction types",
        "anxious habits analysis", "panic avoidance help", "stress response check",
        "anxiety behavior review", "panic reaction patterns", "anxious response help",
        "stress habits analysis", "anxiety avoidance types", "panic behavior check",
        "stress reaction review", "anxiety habits patterns", "anxious avoidance analysis",
        "panic response types", "stress behavior help", "anxiety reaction help",
        "anxious habits review", "panic avoidance analysis", "stress response types",
        "anxiety behavior check", "panic reaction review", "anxious response patterns",
        "stress habits help", "anxiety avoidance patterns", "panic behavior analysis"
    ],
    "Coping_Mechanisms": [
        "anxiety coping strategies", "ways to handle anxiety", "anxiety management tips",
        "coping with panic attacks", "anxiety relief methods", "stress management techniques",
        "anxiety coping tools", "ways to calm anxiety", "anxiety control strategies",
        "managing panic symptoms", "anxiety reduction tips", "stress relief techniques",
        "anxiety handling methods", "ways to reduce anxiety", "panic management strategies",
        "coping with stress", "anxiety calming tips", "stress control techniques",
        "anxiety management tools", "ways to manage anxiety", "panic relief strategies",
        "coping with symptoms", "anxiety reduction methods", "stress handling tips",
        "anxiety relief tools", "ways to cope anxiety", "panic control techniques",
        "managing anxiety symptoms", "stress reduction strategies", "anxiety handling tips",
        "coping techniques anxiety", "ways to handle stress", "panic management methods",
        "anxiety control tools", "stress relief strategies", "anxiety calming techniques",
        "managing panic attacks", "ways to reduce stress", "anxiety relief tips",
        "coping with symptoms", "stress management tools", "panic reduction techniques",
        "anxiety handling strategies", "ways to calm down", "stress control methods",
        "managing anxiety attacks", "panic relief tips", "anxiety reduction tools",
        "coping strategies stress", "ways to handle panic", "anxiety management methods",
        "stress calming techniques", "panic control tips", "anxiety relief strategies",
        "managing symptoms", "ways to manage stress", "anxiety handling tools",
        "coping with attacks", "stress reduction methods", "panic management tips",
        "anxiety control techniques", "ways to cope stress", "anxiety calming strategies",
        "managing stress levels", "panic relief tools", "anxiety reduction methods",
        "coping techniques stress", "ways to handle symptoms", "anxiety management tips",
        "stress control strategies", "panic reduction tools", "anxiety handling techniques",
        "managing anxiety levels", "ways to calm stress", "anxiety relief methods",
        "coping strategies panic", "stress management tips", "anxiety control tools",
        "managing symptoms", "ways to reduce panic", "anxiety calming methods",
        "coping with levels", "panic relief strategies", "stress reduction tools",
        "anxiety handling tips", "ways to manage symptoms", "anxiety management techniques",
        "managing stress", "panic control methods", "anxiety reduction strategies",
        "coping techniques panic", "ways to handle levels", "stress calming tools",
        "anxiety relief tips", "managing anxiety", "panic management techniques",
        "anxiety control methods", "ways to cope symptoms", "stress handling strategies",
        "coping strategies symptoms", "anxiety calming tools", "panic reduction methods",
        "managing levels", "ways to manage panic", "stress relief tips",
        "anxiety handling techniques", "coping with anxiety", "panic control strategies"
    ],
    "Emotional_Responses": [
        "feeling anxious emotions", "emotional anxiety response", "anxiety emotional impact",
        "emotional stress reaction", "anxiety feelings help", "emotional anxiety signs",
        "anxiety emotional symptoms", "feeling stressed emotions", "anxiety emotional state",
        "emotional anxiety impact", "feeling overwhelmed help", "anxiety emotional reaction",
        "emotional stress response", "anxiety feelings check", "emotional anxiety symptoms",
        "feeling anxious help", "anxiety emotional signs", "emotional stress impact",
        "anxiety feelings state", "emotional anxiety reaction", "feeling stressed help",
        "anxiety emotional check", "emotional stress signs", "anxiety feelings impact",
        "emotional anxiety state", "feeling overwhelmed signs", "anxiety emotional symptoms",
        "emotional stress reaction", "anxiety feelings signs", "emotional anxiety impact",
        "feeling anxious state", "anxiety emotional response", "emotional stress symptoms",
        "anxiety feelings reaction", "emotional anxiety signs", "feeling stressed state",
        "anxiety emotional help", "emotional stress impact", "anxiety feelings symptoms",
        "emotional anxiety reaction", "feeling overwhelmed response", "anxiety emotional signs",
        "emotional stress state", "anxiety feelings help", "emotional anxiety symptoms",
        "feeling anxious impact", "anxiety emotional reaction", "emotional stress signs",
        "anxiety feelings state", "emotional anxiety help", "feeling stressed impact",
        "anxiety emotional symptoms", "emotional stress reaction", "anxiety feelings signs",
        "emotional anxiety state", "feeling overwhelmed impact", "anxiety emotional response",
        "emotional stress symptoms", "anxiety feelings reaction", "emotional anxiety signs",
        "feeling anxious symptoms", "anxiety emotional impact", "emotional stress help",
        "anxiety feelings response", "emotional anxiety reaction", "feeling stressed symptoms",
        "anxiety emotional state", "emotional stress signs", "anxiety feelings impact",
        "emotional anxiety help", "feeling overwhelmed state", "anxiety emotional signs",
        "emotional stress reaction", "anxiety feelings symptoms", "emotional anxiety impact",
        "feeling anxious signs", "anxiety emotional response", "emotional stress state",
        "anxiety feelings help", "emotional anxiety signs", "feeling stressed reaction",
        "anxiety emotional symptoms", "emotional stress impact", "anxiety feelings state",
        "emotional anxiety response", "feeling overwhelmed symptoms", "anxiety emotional reaction",
        "emotional stress signs", "anxiety feelings impact", "emotional anxiety state",
        "feeling anxious reaction", "anxiety emotional help", "emotional stress response",
        "anxiety feelings signs", "emotional anxiety impact", "feeling stressed help",
        "anxiety emotional state", "emotional stress symptoms", "anxiety feelings response"
    ],
    "Social_Impact": [
        "anxiety social effects", "social anxiety impact", "anxiety relationship effects",
        "social interaction anxiety", "anxiety friendship impact", "social situation anxiety",
        "anxiety communication effects", "social anxiety help", "anxiety social problems",
        "social relationship anxiety", "anxiety friendship issues", "social anxiety effects",
        "anxiety interaction problems", "social communication anxiety", "anxiety social issues",
        "social relationship effects", "anxiety friendship help", "social anxiety problems",
        "anxiety interaction issues", "social communication effects", "anxiety social help",
        "social relationship problems", "anxiety friendship effects", "social anxiety issues",
        "anxiety interaction help", "social communication problems", "anxiety social effects",
        "social relationship issues", "anxiety friendship problems", "social anxiety help",
        "anxiety interaction effects", "social communication issues", "anxiety social problems",
        "social relationship help", "anxiety friendship issues", "social anxiety effects",
        "anxiety interaction problems", "social communication help", "anxiety social issues",
        "social relationship effects", "anxiety friendship help", "social anxiety problems",
        "anxiety interaction issues", "social communication effects", "anxiety social help",
        "social relationship problems", "anxiety friendship effects", "social anxiety issues",
        "anxiety interaction help", "social communication problems", "anxiety social effects",
        "social relationship issues", "anxiety friendship problems", "social anxiety help",
        "anxiety interaction effects", "social communication issues", "anxiety social problems",
        "social relationship help", "anxiety friendship issues", "social anxiety effects",
        "anxiety interaction problems", "social communication help", "anxiety social issues",
        "social relationship effects", "anxiety friendship help", "social anxiety problems",
        "anxiety interaction issues", "social communication effects", "anxiety social help",
        "social relationship problems", "anxiety friendship effects", "social anxiety issues",
        "anxiety interaction help", "social communication problems", "anxiety social effects",
        "social relationship issues", "anxiety friendship problems", "social anxiety help",
        "anxiety interaction effects", "social communication issues", "anxiety social problems",
        "social relationship help", "anxiety friendship issues", "social anxiety effects",
        "anxiety interaction problems", "social communication help", "anxiety social issues",
        "social relationship effects", "anxiety friendship help", "social anxiety problems",
        "anxiety interaction issues", "social communication effects", "anxiety social help",
        "social relationship problems", "anxiety friendship effects", "social anxiety issues",
        "anxiety interaction help", "social communication problems", "anxiety social effects"
    ],
    "Work_Study_Impact": [
        "anxiety at work", "study anxiety problems", "work performance anxiety",
        "anxiety affecting studies", "work stress impact", "study concentration anxiety",
        "anxiety job performance", "academic anxiety issues", "work anxiety effects",
        "study stress problems", "anxiety career impact", "academic performance anxiety",
        "work concentration issues", "anxiety study effects", "job stress problems",
        "anxiety academic impact", "work anxiety issues", "study performance problems",
        "anxiety job effects", "academic stress impact", "work performance issues",
        "anxiety study problems", "job anxiety effects", "academic concentration issues",
        "work stress effects", "anxiety academic problems", "job performance issues",
        "study anxiety effects", "work concentration problems", "anxiety career effects",
        "academic anxiety impact", "job stress effects", "work performance anxiety",
        "study stress issues", "anxiety job impact", "academic performance problems",
        "work anxiety effects", "study concentration issues", "anxiety career problems",
        "academic stress effects", "job performance anxiety", "work study impact",
        "anxiety academic effects", "study performance anxiety", "job concentration issues",
        "work stress problems", "anxiety study impact", "academic anxiety effects",
        "job stress issues", "work performance problems", "anxiety career impact",
        "study anxiety issues", "academic concentration anxiety", "work job effects",
        "anxiety study problems", "job performance impact", "academic stress issues",
        "work concentration anxiety", "anxiety career effects", "study performance problems",
        "job anxiety impact", "academic concentration issues", "work stress effects",
        "anxiety study issues", "job performance problems", "academic anxiety impact",
        "work concentration problems", "anxiety career issues", "study performance effects",
        "job anxiety problems", "academic stress anxiety", "work study effects",
        "anxiety academic issues", "job concentration problems", "study stress impact",
        "work performance issues", "anxiety career effects", "academic anxiety problems",
        "job stress anxiety", "study concentration effects", "work anxiety impact",
        "anxiety job issues", "academic performance effects", "study stress problems",
        "work career anxiety", "anxiety academic impact", "job performance effects",
        "study concentration issues", "work anxiety problems", "academic stress effects",
        "anxiety job impact", "study performance anxiety", "work concentration effects",
        "academic anxiety issues", "job stress problems", "anxiety career impact",
        "study anxiety effects", "work performance problems", "academic concentration anxiety"
    ],
    "Sleep_Patterns": [
        "anxiety sleep problems", "cant sleep anxiety", "anxiety insomnia help",
        "sleep anxiety issues", "anxiety nighttime problems", "sleep disturbance anxiety",
        "anxiety sleeping patterns", "cant rest anxiety", "sleep anxiety symptoms",
        "anxiety bedtime issues", "sleep problems anxiety", "anxiety rest patterns",
        "insomnia anxiety help", "sleep disturbances", "anxiety sleep quality",
        "nighttime anxiety issues", "sleep pattern problems", "anxiety sleep habits",
        "cant fall asleep anxiety", "sleep anxiety patterns", "anxiety rest issues",
        "insomnia from anxiety", "sleep quality problems", "anxiety bedtime patterns"
    ],
    "Mindfulness_and_Relaxation": [
    "how to meditate",
    "need to calm down",
    "relaxation techniques",
    "breathing exercises",
    "ways to stay present",
    "mindfulness practices",
    "help me relax",
    "meditation tips",
    "grounding techniques",
    "peaceful thoughts",
    "calming exercises",
    "mindful breathing",
    "body scan meditation",
    "relaxation methods",
    "staying present",
    "clear my mind",
    "reduce stress",
    "relax my body",
    "mental peace",
    "quieting thoughts",
    "finding inner peace",
    "calm anxiety naturally",
    "mindfulness for beginners",
    "daily meditation",
    "meditation guidance",
    "relaxation tips",
    "mindful moments",
    "peaceful mindset",
    "stress relief",
    "anxiety calming",
    "meditation practice",
    "relaxation routine",
    "mindful living",
    "tranquil thoughts",
    "inner calmness",
    "peaceful breathing",
    "mindful awareness",
    "relaxation techniques at work",
    "quick meditation",
    "instant calm",
    "mindful walking",
    "peaceful visualization",
    "calming imagery",
    "stress reduction",
    "anxiety relief",
    "meditation basics",
    "relaxation exercises",
    "mindful eating",
    "peaceful mind",
    "calm thoughts",
    "mindfulness tips",
    "relaxation methods",
    "meditation help",
    "stress management",
    "anxiety control",
    "mindful breathing",
    "peaceful moments",
    "calming techniques",
    "meditation guidance",
    "relaxation practice",
    "mindful living tips",
    "tranquility exercises",
    "inner peace methods",
    "peaceful practices",
    "mindful moments",
    "relaxation strategies",
    "meditation routines",
    "quick calm",
    "mindful observation",
    "peaceful exercises",
    "calming practices",
    "stress relief techniques",
    "anxiety management",
    "meditation steps",
    "relaxation guide",
    "mindful practice",
    "peaceful methods",
    "calm exercises",
    "mindfulness routine",
    "relaxation tips",
    "meditation advice",
    "stress reduction methods",
    "anxiety relief techniques",
    "mindful awareness practices",
    "peaceful strategies",
    "calming methods",
    "meditation techniques",
    "relaxation exercises",
    "mindful living advice",
    "tranquil practices",
    "inner peace techniques",
    "peaceful routines",
    "mindful strategies",
    "relaxation methods",
    "meditation practices",
    "quick relaxation",
    "mindful techniques",
    "peaceful exercises",
    "calming strategies",
    "stress management tips",
    "anxiety control methods",
    "meditation guidance",
    "relaxation strategies",
    "mindful moments practice",
    "peaceful techniques"
  ],
  "Severity_and_Frequency": [
    "anxiety level check",
    "how often anxious",
    "panic attack frequency",
    "anxiety symptoms severity",
    "daily anxiety rating",
    "anxiety patterns",
    "panic frequency",
    "symptom tracking",
    "anxiety intensity",
    "anxiety occurrence",
    "anxiety monitoring",
    "symptom severity",
    "panic attack patterns",
    "anxiety frequency check",
    "symptom intensity",
    "anxiety tracking",
    "panic monitoring",
    "anxiety assessment",
    "symptom patterns",
    "anxiety measurement",
    "panic severity",
    "anxiety check-in",
    "symptom frequency",
    "anxiety intensity scale",
    "panic tracking",
    "anxiety monitoring system",
    "symptom assessment",
    "anxiety pattern check",
    "panic intensity",
    "anxiety severity scale",
    "symptom monitoring",
    "anxiety frequency log",
    "panic assessment",
    "anxiety intensity check",
    "symptom tracking system",
    "anxiety pattern monitoring",
    "panic frequency check",
    "anxiety severity assessment",
    "symptom intensity scale",
    "anxiety tracking log",
    "panic monitoring system",
    "anxiety assessment scale",
    "symptom pattern check",
    "anxiety measurement tool",
    "panic severity scale",
    "anxiety check system",
    "symptom frequency log",
    "anxiety intensity monitor",
    "panic tracking system",
    "anxiety monitoring log",
    "symptom assessment scale",
    "anxiety pattern tracker",
    "panic intensity check",
    "anxiety severity monitor",
    "symptom monitoring system",
    "anxiety frequency tracker",
    "panic assessment scale",
    "anxiety intensity log",
    "symptom tracking log",
    "anxiety pattern assessment",
    "panic frequency monitor",
    "anxiety severity tracker",
    "symptom intensity monitor",
    "anxiety tracking system",
    "panic monitoring log",
    "anxiety assessment log",
    "symptom pattern tracker",
    "anxiety measurement system",
    "panic severity monitor",
    "anxiety check tracker",
    "symptom frequency monitor",
    "anxiety intensity tracking",
    "panic tracking log",
    "anxiety monitoring scale",
    "symptom assessment log",
    "anxiety pattern monitoring",
    "panic intensity tracker",
    "anxiety severity logging",
    "symptom monitoring log",
    "anxiety frequency assessment",
    "panic assessment log",
    "anxiety intensity system",
    "symptom tracking scale",
    "anxiety pattern check",
    "panic frequency tracker",
    "anxiety severity scale",
    "symptom intensity log",
    "anxiety tracking monitor",
    "panic monitoring scale",
    "anxiety assessment system",
    "symptom pattern log",
    "anxiety measurement log",
    "panic severity tracker",
    "anxiety check log",
    "symptom frequency scale",
    "anxiety intensity assessment",
    "panic tracking monitor",
    "anxiety monitoring tracker",
    "symptom assessment system",
    "anxiety pattern scale",
    "panic intensity log",
    "anxiety severity system",
    "symptom monitoring scale",
    "anxiety frequency monitor",
    "panic assessment tracker",
    "anxiety intensity scale",
    "symptom tracking monitor"
  ],
  "Environmental_Triggers": [
    "work stress triggers",
    "social anxiety causes",
    "crowd anxiety trigger",
    "noise sensitivity",
    "environmental stressors",
    "anxiety at home",
    "workplace anxiety",
    "public transport fears",
    "social gathering stress",
    "traffic anxiety",
    "weather anxiety",
    "classroom anxiety",
    "shopping anxiety",
    "restaurant stress",
    "meeting anxiety",
    "phone anxiety",
    "performance anxiety",
    "travel anxiety",
    "elevator fears",
    "public speaking stress",
    "driving anxiety",
    "hospital anxiety",
    "flight anxiety",
    "stage fright",
    "exam stress",
    "interview anxiety",
    "deadline pressure",
    "presentation anxiety",
    "family gathering stress",
    "party anxiety",
    "dating anxiety",
    "gym anxiety",
    "doctor visit stress",
    "workplace meetings",
    "public bathroom anxiety",
    "restaurant anxiety",
    "mall anxiety",
    "cinema stress",
    "concert anxiety",
    "sports performance",
    "morning anxiety",
    "nighttime anxiety",
    "commute stress",
    "parking anxiety",
    "waiting room stress",
    "classroom presentation",
    "group project anxiety",
    "public performance",
    "social media stress",
    "video call anxiety",
    "workplace competition",
    "family dinner stress",
    "holiday anxiety",
    "vacation stress",
    "moving anxiety",
    "job interview stress",
    "first day anxiety",
    "meeting new people",
    "public speaking event",
    "performance review",
    "deadline anxiety",
    "test taking stress",
    "social event anxiety",
    "crowd situations",
    "noise triggers",
    "bright light sensitivity",
    "temperature stress",
    "confined spaces",
    "open spaces anxiety",
    "height anxiety",
    "water anxiety",
    "animal anxiety",
    "storm anxiety",
    "darkness fears",
    "sleeping anxiety",
    "eating in public",
    "writing anxiety",
    "reading aloud",
    "phone calls",
    "video recording",
    "photo taking",
    "social media posting",
    "public transport",
    "elevator riding",
    "escalator anxiety",
    "bridge crossing",
    "tunnel anxiety",
    "highway driving",
    "parking stress",
    "traffic jams",
    "time pressure",
    "decision making",
    "financial stress",
    "health anxiety",
    "relationship stress",
    "work deadlines",
    "performance pressure",
    "competition anxiety",
    "evaluation stress",
    "criticism anxiety",
    "conflict situations",
    "confrontation fear",
    "authority figures",
    "social rejection",
    "perfectionism stress",
    "change anxiety",
    "uncertainty stress",
    "future anxiety",
    "past trauma triggers",
    "memory anxiety",
    "identity stress"
  ],
  "Past_Experiences": [
    "childhood anxiety",
    "past trauma",
    "previous panic attacks",
    "anxiety history",
    "traumatic events",
    "past experiences",
    "anxiety patterns",
    "old fears",
    "previous therapy",
    "anxiety development",
    "past triggers",
    "childhood fears",
    "historical anxiety",
    "anxiety origins",
    "past treatment",
    "anxiety evolution",
    "previous symptoms",
    "anxiety background",
    "past coping",
    "anxiety journey",
    "previous struggles",
    "anxiety timeline",
    "past management",
    "anxiety progression",
    "previous episodes",
    "anxiety roots",
    "past challenges",
    "anxiety development",
    "previous experiences",
    "anxiety history review",
    "past anxiety patterns",
    "previous conditions",
    "anxiety background check",
    "past symptoms",
    "anxiety chronicle",
    "previous incidents",
    "anxiety story",
    "past situations",
    "anxiety development path",
    "previous occurrences",
    "anxiety timeline review",
    "past episodes",
    "anxiety progression path",
    "previous cases",
    "anxiety background story",
    "past conditions",
    "anxiety history check",
    "previous patterns",
    "anxiety origin story",
    "past incidents",
    "anxiety development review",
    "previous situations",
    "anxiety chronicle review",
    "past cases",
    "anxiety timeline check",
    "previous stories",
    "anxiety progression review",
    "past occurrences",
    "anxiety background path",
    "previous episodes review",
    "anxiety origin check",
    "past patterns review",
    "anxiety development story",
    "previous incidents check",
    "anxiety history path",
    "past situations review",
    "anxiety chronicle path",
    "previous cases review",
    "anxiety timeline story",
    "past episodes check",
    "anxiety progression story",
    "previous patterns check",
    "anxiety background review",
    "past incidents path",
    "anxiety origin path",
    "previous situations check",
    "anxiety development check",
    "past cases path",
    "anxiety history story",
    "previous occurrences review",
    "anxiety chronicle story",
    "past patterns path",
    "anxiety timeline path",
    "previous episodes story",
    "anxiety progression check",
    "past incidents story",
    "anxiety background story",
    "previous situations path",
    "anxiety origin review",
    "past cases story",
    "anxiety development path",
    "previous patterns story",
    "anxiety history check",
    "past occurrences path",
    "anxiety chronicle check",
    "previous incidents path",
    "anxiety timeline review",
    "past episodes path",
    "anxiety progression path",
    "previous situations story",
    "anxiety origin story",
    "past patterns story",
    "anxiety development review",
    "previous cases path",
    "anxiety history path",
    "past incidents check"
  ],
  "Professional_Help": [
    "find therapist",
    "counseling options",
    "therapy benefits",
    "mental health help",
    "anxiety specialist",
    "professional support",
    "counselor search",
    "treatment options",
    "therapy costs",
    "mental health resources",
    "anxiety treatment",
    "professional guidance",
    "counseling benefits",
    "therapy types",
    "mental health support",
    "anxiety counseling",
    "professional therapy",
    "counselor recommendations",
    "treatment plans",
    "therapy sessions",
    "mental health care",
    "anxiety specialists",
    "professional counseling",
    "therapy advice",
    "mental health treatment",
    "anxiety professionals",
    "counseling services",
    "therapy resources",
    "mental health specialists",
    "anxiety help",
    "professional treatment",
    "counseling support",
    "therapy options",
    "mental health counseling",
    "anxiety therapy",
    "professional advice",
    "counseling types",
    "therapy plans",
    "mental health professionals",
    "anxiety treatment options",
    "professional support services",
    "counseling resources",
    "therapy recommendations",
    "mental health therapy",
    "anxiety counseling options",
    "professional guidance services",
    "therapy support",
    "mental health treatment options",
    "anxiety professional help",
    "counseling plans",
    "therapy services",
    "mental health advice",
    "anxiety specialist search",
    "professional counseling options",
    "therapy treatment",
    "mental health support services",
    "anxiety therapy options",
    "professional resources",
    "counseling advice",
    "therapy specialists",
    "mental health plans",
    "anxiety treatment services",
    "professional therapy options",
    "counseling treatment",
    "therapy help",
    "mental health specialists search",
    "anxiety counseling services",
    "professional support options",
    "therapy guidance",
    "mental health resources search",
    "anxiety professional support",
    "counseling specialists",
    "therapy treatment options",
    "mental health counseling services",
    "anxiety therapy services",
    "professional help options",
    "counseling guidance",
    "therapy advice services",
    "mental health treatment services",
    "anxiety specialist options",
    "professional counseling services",
    "therapy support options",
    "mental health guidance",
    "anxiety treatment specialists",
    "professional therapy services",
    "counseling help",
    "therapy resources search",
    "mental health help options",
    "anxiety counseling specialists",
    "professional support search",
    "therapy guidance services",
    "mental health specialist options",
    "anxiety professional services",
    "counseling support options",
    "therapy treatment services",
    "mental health counseling options",
    "anxiety therapy specialists",
    "professional help services",
    "counseling resources search",
    "therapy specialist options",
    "mental health treatment specialists",
    "anxiety support services",
    "professional guidance options",
    "counseling treatment services",
    "therapy help options",
    "mental health professional search"
  ],
  "Motivational_Support": [
    "need encouragement",
    "feeling unmotivated",
    "motivation help",
    "positive thinking",
    "confidence boost",
    "encouragement needed",
    "staying motivated",
    "positive mindset",
    "self motivation",
    "motivation tips",
    "encouraging words",
    "positive attitude",
    "confidence building",
    "motivation boost",
    "encouraging thoughts",
    "positive energy",
    "self confidence",
    "motivation advice",
    "encouraging messages",
    "positive thinking help",
    "confidence tips",
    "motivation support",
    "encouraging support",
    "positive mindset help",
    "self esteem",
    "motivation guidance",
    "encouraging advice",
    "positive attitude help",
    "confidence advice",
    "motivation ideas",
    "encouraging ideas",
    "positive energy boost",
    "self worth",
    "motivation strategies",
    "encouraging strategies",
    "positive thinking tips",
    "confidence strategies",
    "motivation techniques",
    "encouraging techniques",
    "positive mindset tips",
    "self belief",
    "motivation methods",
    "encouraging methods",
    "positive attitude tips",
    "confidence methods",
  ],
  "Self_Awareness": [
    "how am i feeling",
    "check my mood",
    "track my emotions",
    "understand my anxiety",
    "identify my triggers",
    "what causes my stress",
    "recognize anxiety signs",
    "monitor my progress",
    "track panic attacks",
    "emotional patterns",
    "why am i anxious",
    "anxiety journal",
    "mood tracking",
    "feeling overwhelmed",
    "stress levels",
    "rate my anxiety",
    "document triggers",
    "analyze my thoughts",
    "notice body signals",
    "physical symptoms",
    "emotional state",
    "record my day",
    "anxiety intensity",
    "mood fluctuations",
    "stress indicators",
    "panic symptoms",
    "anxiety patterns",
    "emotional awareness",
    "self reflection",
    "mindful check in",
    "body scan",
    "thought patterns",
    "identify emotions",
    "track sleep quality",
    "energy levels",
    "stress response",
    "emotional triggers",
    "anxiety cycle",
    "mood history",
    "behavioral patterns",
    "symptom diary",
    "emotional intelligence",
    "self observation",
    "mental state",
    "anxiety profile",
    "daily reflection",
    "emotional journey",
    "stress tracking",
    "anxiety monitoring",
    "thought awareness",
    "emotional check",
    "trigger identification",
    "anxiety awareness",
    "mood patterns",
    "stress symptoms",
    "anxiety insights",
    "emotional trends",
    "self monitoring",
    "anxiety diary",
    "thought tracking",
    "mood recognition",
    "stress awareness",
    "anxiety history",
    "emotional mapping",
    "symptom tracking",
    "anxiety log",
    "mood monitoring",
    "stress diary",
    "thought journal",
    "emotional record",
    "trigger log",
    "anxiety check",
    "mood log",
    "stress patterns",
    "thought diary",
    "emotional diary",
    "trigger diary",
    "anxiety tracker",
    "mood checker",
    "stress log",
    "thought log",
    "emotional log",
    "trigger tracker",
    "anxiety monitor",
    "mood tracker",
    "stress monitor",
    "thought monitor",
    "emotional tracker",
    "trigger monitor",
    "anxiety record",
    "mood diary",
    "stress tracker",
    "thought tracker",
    "emotional monitor",
    "trigger patterns",
    "anxiety patterns",
    "mood patterns",
    "stress analysis",
    "thought analysis",
    "emotional analysis",
    "trigger analysis",
    "anxiety trends",
    "mood trends",
    "stress trends",
    "thought trends",
    "emotional trends",
    "trigger trends"
  ],
  "Resources_and_Education": [
    "anxiety articles",
    "learn about anxiety",
    "anxiety resources",
    "mental health tips",
    "anxiety education",
    "stress management guides",
    "anxiety information",
    "mental health resources",
    "anxiety research",
    "coping strategies",
    "anxiety facts",
    "mental health articles",
    "anxiety guides",
    "stress relief tips",
    "anxiety learning",
    "mental health education",
    "anxiety knowledge",
    "stress management info",
    "anxiety materials",
    "mental health guides",
    "anxiety understanding",
    "stress education",
    "anxiety insights",
    "mental health learning",
    "anxiety awareness",
    "stress resources",
    "anxiety tools",
    "mental health knowledge",
    "anxiety support",
    "stress information",
    "anxiety help",
    "mental health materials",
    "anxiety management",
    "stress guidance",
    "anxiety guidance",
    "mental health insights",
    "anxiety tips",
    "stress understanding",
    "anxiety basics",
    "mental health awareness",
    "anxiety explained",
    "stress knowledge",
    "anxiety overview",
    "mental health tools",
    "anxiety fundamentals",
    "stress basics",
    "anxiety principles",
    "mental health support",
    "anxiety concepts",
    "stress help",
    "anxiety studies",
    "mental health management",
    "anxiety science",
    "stress tips",
    "anxiety research",
    "mental health information",
    "anxiety literature",
    "stress concepts",
    "anxiety reading",
    "mental health basics",
    "anxiety library",
    "stress studies",
    "anxiety resources",
    "mental health principles",
    "anxiety materials",
    "stress overview",
    "anxiety documents",
    "mental health concepts",
    "anxiety references",
    "stress fundamentals",
    "anxiety sources",
    "mental health studies",
    "anxiety knowledge base",
    "stress science",
    "anxiety database",
    "mental health research",
    "anxiety collection",
    "stress literature",
    "anxiety repository",
    "mental health reading",
    "anxiety archive",
    "stress library",
    "anxiety information",
    "mental health resources",
    "anxiety education",
    "stress materials",
    "anxiety learning",
    "mental health documents",
    "anxiety understanding",
    "stress references",
    "anxiety awareness",
    "mental health sources",
    "anxiety knowledge",
    "stress knowledge base",
    "anxiety insights",
    "mental health database",
    "anxiety basics",
    "stress collection",
    "anxiety fundamentals",
    "mental health repository",
    "anxiety principles",
    "stress archive",
    "anxiety concepts",
    "mental health information",
    "anxiety studies",
    "stress education",
    "anxiety science",
    "mental health learning",
    "anxiety literature",
    "stress understanding"
  ],
  "Real_Time_Techniques": [
    "breathing exercise",
    "calm down now",
    "quick anxiety relief",
    "grounding techniques",
    "panic help",
    "immediate relief",
    "anxiety exercise",
    "calming methods",
    "stress relief now",
    "anxiety reduction",
    "relaxation techniques",
    "mindfulness exercise",
    "emergency calm",
    "instant peace",
    "anxiety control",
    "quick meditation",
    "rapid relaxation",
    "stress reduction",
    "anxiety management",
    "calm breathing",
    "panic reduction",
    "quick calm",
    "anxiety relief",
    "instant meditation",
    "stress control",
    "breathing help",
    "immediate calm",
    "anxiety ease",
    "quick peace",
    "stress relief",
    "panic control",
    "instant relief",
    "anxiety calm",
    "quick relax",
    "stress ease",
    "breathing technique",
    "immediate peace",
    "anxiety peace",
    "quick calm down",
    "stress reduction",
    "panic ease",
    "instant calm",
    "anxiety relax",
    "quick peace",
    "stress control",
    "breathing help",
    "immediate relief",
    "anxiety control",
    "quick meditation",
    "stress calm",
    "panic relief",
    "instant peace",
    "anxiety reduction",
    "quick relaxation",
    "stress ease",
    "breathing exercise",
    "immediate calm",
    "anxiety peace",
    "quick relief",
    "stress relief",
    "panic control",
    "instant relax",
    "anxiety calm",
    "quick peace",
    "stress reduction",
    "breathing technique",
    "immediate relief",
    "anxiety ease",
    "quick calm",
    "stress control",
    "panic ease",
    "instant calm",
    "anxiety relief",
    "quick meditation",
    "stress peace",
    "breathing help",
    "immediate peace",
    "anxiety control",
    "quick relaxation",
    "stress ease",
    "panic relief",
    "instant relief",
    "anxiety reduction",
    "quick calm",
    "stress calm",
    "breathing exercise",
    "immediate calm",
    "anxiety peace",
    "quick relief",
    "stress relief",
    "panic control",
    "instant peace",
    "anxiety ease",
    "quick meditation",
    "stress reduction",
    "breathing technique",
    "immediate relief",
    "anxiety calm",
    "quick relaxation",
    "stress control",
    "panic ease",
    "instant calm",
    "anxiety relief",
    "quick peace",
    "stress ease",
    "breathing help",
    "immediate peace",
    "anxiety control"
  ],
  "Depression_Symptoms": [
    "feeling hopeless", "symptoms of depression", "signs of depression", 
    "chronic sadness", "feeling numb", "lack of motivation", 
    "feeling worthless", "excessive guilt", "feeling empty", 
    "difficulty concentrating", "loss of interest", "sleep problems", 
    "feeling disconnected", "low energy", "increased irritability", 
    "social withdrawal", "feeling like a burden", "hopeless thoughts", 
    "constant fatigue", "negative thinking", "feeling stuck", 
    "mood swings", "feeling overwhelmed", "feeling inadequate", 
    "thoughts of isolation", "feeling emotionally drained", "inability to feel joy", "I feel depressed and hopeless", "What are the symptoms of depression?", 
    "I’ve been feeling chronically sad and depressed", "What are the signs I might be depressed?",
    "I’m feeling numb and disconnected, could I be depressed?", "Is it normal to feel worthless when I'm depressed?",
    "Why do I feel empty and depressed all the time?", "I've been having trouble concentrating and I feel depressed",
    "I'm constantly tired and depressed, is this normal?", "Why do I feel like I’ve lost interest in everything? Could this be depression?",
    "I feel so disconnected from others, could this be depression?", "I've been feeling increasingly irritable and depressed",
    "I'm withdrawing from social activities, is that a sign of depression?", "I feel like a burden to everyone, is this depression?",
    "I've been feeling so tired and depressed, it’s affecting my daily life", "Can feeling overwhelmed and depressed be connected?",
    "I can't escape my negative thoughts, am I depressed?", "I feel stuck, could this be because of depression?"

],
"Depression_Coping_Strategies": [
    "coping with depression", "ways to manage depression", "depression relief methods",
    "how to handle depression", "dealing with depressive episodes", "managing low moods", 
    "tips to manage depression", "self-care for depression", "mental health recovery tips", 
    "coping mechanisms for depression", "how to lift your mood", "strategies to reduce sadness", 
    "mental health coping strategies", "mindfulness for depression", "techniques to overcome depression",
    "emotional regulation for depression", "dealing with hopelessness", "managing negative thoughts", 
    "overcoming feelings of worthlessness", "how to deal with sadness", "mental health coping tools", 
    "building resilience against depression", "depression relief techniques", "how to shift depressive thoughts",
    "supporting yourself through depression", "mental health self-care practices", "What can I do if I am depressed?", "How can I handle depression on my own?",
    "I’m depressed and need help managing my emotions", "What are some effective coping strategies for dealing with depression?",
    "How can I lift my mood when I’m feeling depressed?", "I feel so depressed, what can I do to manage it better?",
    "Are there any good mental health recovery tips for someone who is depressed?", "What are some self-care strategies for someone who feels depressed?",
    "How can I overcome the feelings of worthlessness that come with depression?", "What mindfulness techniques can help with depression?",
    "How can I overcome my negative thoughts when I’m depressed?", "How can I feel better if I’m stuck in depression?",
    "What can I do to support myself through depression?", "How can I build resilience if I’m feeling depressed?",
    "What strategies can I use to cope with the emotional toll of depression?"

],
"Seeking_Professional_Help": [
    "therapy for depression", "how to find a therapist", "talking to a counselor", 
    "mental health professional", "finding help for depression", "seeking therapy for depression",
    "looking for depression support", "how to get professional help for depression", 
    "depression treatment options", "psychologist for depression", "getting help for depression",
    "seeking support for mental health", "should I see a therapist for depression?", "help with depressive feelings", 
    "where to get help for depression", "depression counseling services", "when to seek professional help",  "Should I see a therapist if I am depressed?", "How do I find a therapist for depression?",
    "I’ve been feeling depressed for weeks, how can I get professional help?", "What kind of therapy can help with depression?",
    "Is therapy necessary when you’re feeling depressed?", "How can I get professional support for my depression?",
    "What should I do if I am deeply depressed and need help?", "Where can I get help for depression?",
    "What are my options for therapy when I feel severely depressed?", "Can a psychologist help if I am depressed?",
    "How do I know if I need therapy for my depression?", "Should I see a therapist if I’m constantly feeling depressed?",
    "When should I seek professional help for depression?", "I’ve been struggling with depression, how can a therapist assist me?",
    "What options do I have if I’m seeking therapy for depression?"

],
"Depression_Support_Network": [
    "talking to family about depression", "support from friends during depression", 
    "finding support for depression", "how to talk to someone about depression", 
    "building a support system", "finding a support group for depression", 
    "depression support networks", "connecting with others who understand depression",
    "support for people with depression", "getting help from loved ones", 
    "talking to someone about feeling depressed", "peer support for depression", 
    "how to ask for help with depression", "support for managing depression",  "How do I talk to someone when I am feeling depressed?", "How can my family support me if I’m depressed?",
    "What’s the best way to ask for help when I am depressed?", "How can I talk to my friends about my depression?",
    "Can a support group help when I am depressed?", "How can I build a support network when I’m feeling depressed?",
    "Where can I find a support group for depression?", "How can I find people who understand what it feels like to be depressed?",
    "How can I talk about my depression with people who care?", "What’s the best way to open up about being depressed?",
    "What are the benefits of peer support when I’m depressed?", "How can I find people who can help when I feel depressed?"

],
"Depression_Affirmations": [
    "positive affirmations for depression", "affirmations for overcoming sadness", 
    "affirmations to lift your mood", "boosting self-esteem with affirmations", 
    "powerful affirmations for depression", "I am not defined by my depression", 
    "I can overcome this", "affirmations to help with hopelessness", 
    "I am worthy of love and care", "I am capable of healing", 
    "affirmations for building strength", "I am strong enough to face this", 
    "every day is a new opportunity", "I can get through this", "I am feeling depressed, but I can get through this", "I am not defined by my depression",
    "Even though I am depressed, I know I have the strength to heal", "I am worthy of love and care despite my depression",
    "Every day I face my depression, I am getting stronger", "My depression doesn’t control me, I can overcome it",
    "Though I feel depressed, I believe things can get better", "Even when I’m depressed, I am capable of healing",
    "I deserve peace, even when I feel depressed", "I am not alone in my depression, I can seek help",
    "Each step I take, no matter how small, brings me closer to overcoming depression"
 
],
"Depression_Exercise_Tips": [
    "exercises for depression", "how exercise helps with depression", 
    "physical activity to combat depression", "how to stay active with depression", 
    "simple exercises for depression", "using exercise to boost mood", 
    "depression and physical activity", "exercise routines for depression", 
    "how to use exercise to fight sadness", "staying active during depression", 
    "benefits of exercise for mental health", "low-impact exercises for depression", "How can exercise help when I’m feeling depressed?", "What are some exercises I can do when I’m depressed?",
    "I’m depressed, what physical activities can help boost my mood?", "How can I stay active when I feel depressed?",
    "What exercises help fight feelings of depression?", "How can a workout routine help if I am feeling depressed?",
    "Can physical activity reduce the effects of depression?", "What low-impact exercises can help when I’m feeling depressed?",
    "How can movement and exercise help when I’m stuck in depression?", "Can yoga help when I’m feeling depressed?",
    "Is walking a good option for someone who feels depressed?", "How can exercise help me cope with depression and sadness?"
 
],
"Depression_Sleep_Tips": [
    "how to improve sleep with depression", "sleep hygiene for depression", 
    "tips for better sleep with depression", "how to sleep better when depressed", 
    "depression and sleep problems", "overcoming insomnia with depression", 
    "tips for restful sleep during depression", "how to get more sleep when depressed",
    "sleep strategies for people with depression", "improving sleep habits during depression",  "How can I improve my sleep when I’m depressed?", "I’ve been having trouble sleeping due to depression, what can I do?",
    "What are some sleep tips when you feel depressed?", "How can sleep hygiene help when I’m feeling depressed?",
    "What should I do to get better sleep if I’m depressed?", "How can I overcome insomnia caused by depression?",
    "I feel depressed and tired all the time, what can help me sleep better?", "Can a better sleep routine help me manage depression?",
    "How can I improve my sleep habits when dealing with depression?", "What relaxation techniques can help me sleep when I’m depressed?",
    "What are some natural ways to improve sleep when you feel depressed?"
 
],
"Depression_Mindfulness_Techniques": [
    "mindfulness for depression", "how to practice mindfulness with depression", 
    "meditation for depression", "using mindfulness to manage depression", 
    "breathing exercises for depression", "grounding techniques for depression", 
    "how to be mindful during depressive episodes", "mindful ways to cope with sadness", 
    "meditation for mental health", "how mindfulness can help with depression", 
    "mindfulness exercises for emotional regulation", "how mindfulness reduces stress and depression", "How can mindfulness help when I’m feeling depressed?", "What are some mindfulness techniques to manage depression?",
    "Can meditation help with depression?", "How do breathing exercises help when you’re depressed?",
    "How can grounding techniques help when I feel depressed?", "What mindfulness practices can help when I am depressed?",
    "How can mindfulness shift my mood if I’m feeling depressed?", "How can I use mindfulness to cope with depression?",
    "What is mindfulness and how can it help with depression?", "How can I apply mindfulness to my depression?"
 
],
  "Feedback_and_Improvement": [
    "rate experience",
    "provide feedback",
    "suggest improvements",
    "share thoughts",
    "app review",
    "feature request",
    "report issue",
    "give rating",
    "improvement ideas",
    "user feedback",
    "rate app",
    "suggest features",
    "report bug",
    "share experience",
    "app feedback",
    "improvement suggestions",
    "user review",
    "rate service",
    "suggest changes",
    "report problem",
    "share opinion",
    "app suggestion",
    "improvement request",
    "user input",
    "rate quality",
    "suggest update",
    "report error",
    "share feedback",
    "app improvement",
    "feature feedback",
    "user suggestion",
    "rate usefulness",
    "suggest enhancement",
    "report glitch",
    "share review",
    "app rating",
    "improvement feedback",
    "user experience",
    "rate effectiveness",
    "suggest addition",
    "report difficulty",
    "share suggestion",
    "app comment",
    "feature suggestion",
    "user rating",
    "rate satisfaction",
    "suggest upgrade",
    "report confusion",
    "share opinion",
    "app review",
    "improvement idea",
    "user comment",
    "rate helpfulness",
    "suggest change",
    "report problem",
    "share thought",
    "app feedback",
    "feature request",
    "user input",
    "rate quality",
    "suggest update",
    "report issue",
    "share experience",
    "app suggestion",
    "improvement request",
    "user review",
    "rate service",
    "suggest enhancement",
    "report bug",
    "share feedback",
    "app improvement",
    "feature feedback",
    "user suggestion",
    "rate usefulness",
    "suggest addition",
    "report error",
    "share review",
    "app rating",
    "improvement feedback",
    "user experience",
    "rate effectiveness",
    "suggest upgrade",
    "report glitch",
    "share suggestion",
    "app comment",
    "feature suggestion",
    "user rating",
    "rate satisfaction",
    "suggest change",
    "report difficulty",
    "share opinion",
    "app review",
    "improvement idea",
    "user comment",
    "rate helpfulness",
    "suggest update",
    "report confusion",
    "share thought",
    "app feedback",
    "feature request",
    "user input",
    "rate quality",
    "suggest enhancement",
    "report problem",
    "share experience",
    "app suggestion",
    "improvement request",
    "user review"
  ],
    "Feeling_Overwhelmed_Stressed": [
    "I’m feeling really overwhelmed.",
    "I feel like I can’t handle everything.",
    "I’m super stressed out right now.",
    "I can’t keep up with everything.",
    "Everything feels so overwhelming.",
    "I’m having a hard time managing everything.",
    "This is just too much for me.",
    "I feel like I’m drowning in stress.",
    "I’m so stressed I can’t think straight.",
    "I’m really struggling with stress.",
    "This is too much to deal with.",
    "I feel like everything is crashing down.",
    "I'm feeling overwhelmed with life right now.",
    "I just can't seem to handle everything.",
    "Everything’s getting on top of me.",
    "I'm feeling way too stressed.",
    "I don’t know how to handle all this pressure.",
    "I’m stressed out to the max.",
    "I feel completely overwhelmed.",
    "There’s too much going on right now.",
    "I can't manage all the things I'm dealing with.",
    "Everything seems too overwhelming right now.",
    "I can’t take all this stress anymore.",
    "I feel like I’m running out of time.",
    "Everything is just too much for me to handle.",
    "I’m exhausted from being stressed all the time.",
    "I feel so stressed, I don’t know where to start.",
     "I'm struggling to juggle my responsibilities and it's overwhelming.",
  "Balancing school, family, friends, and spiritual life is really exhausting.",
  "I'm trying to achieve so many goals but I feel like I can't keep up.",
  "How do I manage my time when I have so many things on my plate?",
  "I feel overwhelmed with everything happening in my life right now.",
  "I can't balance my personal goals with everything else in my life.",
  "I'm under a lot of pressure, I don’t know how to balance work, school, and my personal life.",
  "I'm feeling overwhelmed with the constant demands from my family and friends.",
  "It's difficult to balance my spiritual life and daily responsibilities.",
  "How do I avoid burnout while trying to achieve all my goals?",
  "How can I manage my time between school, family, and personal goals?",
  "I feel like I’m failing to meet all my obligations and it’s really stressing me out.",
  "I'm overwhelmed with trying to meet my academic goals and still maintain a social life.",
  "How do I prioritize between my family, friends, and personal goals?",
  "I just can’t keep up with everything—work, school, personal life, and my spiritual growth.",
  "I’m always stressed about balancing my goals with my responsibilities.",
  "I feel constantly pulled in multiple directions and I’m starting to burn out.",
  "What can I do to feel less overwhelmed when trying to achieve my goals?",
  "I’m tired of trying to juggle so many things—how can I feel more in control?",
  "My mental health is suffering due to the pressure of balancing all my obligations.",
  "How do I balance my spiritual practices with my day-to-day responsibilities?",
  ],
"Journaling_and_Self_Reflection": [
    "I write in my journal every day.",
    "What are some good journaling prompts?",
    "I’m trying to get better at journaling.",
    "Can you suggest some self-reflection prompts?",
    "I want to start journaling.",
    "I need journaling ideas.",
    "What should I write in my journal?",
    "I journal every day",
    "I write in my journal daily",
    "I keep a daily journal",
    "I write about my day every day",
    "I journal regularly",
    "I maintain a journal every day",
    "I do daily journaling",
    "I write my thoughts down every day",
    "I document my experiences daily",
    "I express myself in writing each day",
    "I record my feelings daily",
    "I make journal entries every day",
    "I write in a notebook each day",
    "My habit is journaling every day",
    "I have a daily writing routine",
    "I capture my thoughts every day",
    "I reflect in my journal daily",
    "I track my day in a journal",
    "I write in a diary daily",
    "I use journaling as a daily habit",
    "I journal to track my mood",
    "I make time to journal each day",
    "Journaling is part of my routine",
    "I try to write every day",
    "I document my experiences with journaling",
    "Journaling has become a part of my daily life",
    "I express my emotions through journaling",
    "I reflect on my thoughts daily",
    "Journaling is my self-care activity",
    "I write down everything that happens in my life",
    "I’m committed to journaling every day",
    "Writing helps me unwind every day",
    "I write about my personal growth every day",
    "I write down my successes and failures daily",
    "I feel calm after journaling",
    "I reflect on my feelings in my journal every day",
    "I record both positive and negative thoughts in my journal",
    "I use journaling as a tool for mental health",
    "Journaling helps me process my emotions daily",
    "I turn to my journal to sort my thoughts",
    "Writing every day brings me peace",
    "I use journaling for self-reflection",
    "I document my daily challenges in my journal",
    "I’m improving myself through journaling daily",
    "I write my personal experiences down every day",
    "Journaling helps me manage stress",
    "I write to understand my feelings",
    "My journal is my emotional outlet",
    "I record my thoughts to understand myself better",
    "I make journal entries to track my progress",
    "I’ve built a journaling habit for mental clarity",
    "I write about my goals and achievements daily",
    "I track my thoughts in my journal every day",
    "I write in my journal for emotional balance",
    "Journaling helps me clear my mind daily",
    "I’ve been journaling to improve my mindset",
    "Writing daily helps me deal with anxiety",
    "I write to release my daily frustrations",
    "My journal is a safe space for my thoughts",
    "I use journaling to improve my mental health",
    "Journaling daily has become therapeutic for me",
    "Writing helps me make sense of my emotions",
    "Journaling allows me to reflect on my day",
    "I feel lighter after writing in my journal every day",
    "I write down the highs and lows of my day",
    "Journaling helps me feel grounded",
    "I’m grateful for the journaling practice I’ve built",
    "My journal helps me stay focused on my goals",
    "I can express myself freely in my journal",
    "I write about my fears and hopes every day",
    "Writing helps me deal with overwhelming thoughts",
    "Journaling every day helps me heal emotionally",
    "I turn to my journal when I need clarity",
    "I use journaling as a tool for growth",
    "I’ve been journaling to track my habits",
    "I like to write in my journal after a long day",
    "Writing daily helps me organize my thoughts",
    "I document my mental health journey through journaling",
    "I reflect on my emotions by journaling each day",
    "Writing helps me process my experiences better",
    "I’ve made journaling a part of my morning routine",
    "I find peace in writing down my feelings",
    "I take time to journal daily as part of my self-care",
    "My journal is a place for me to vent and release",
    "I write down my goals for the day in my journal",
    "Journaling every day helps me stay organized",
    "I use journaling to help me understand my thoughts",
    "I write about my daily victories and challenges",
    "Journaling is a habit I’ve developed for my well-being",
    "I use journaling to reflect on personal growth",
    "I make journaling part of my self-awareness journey",
    "I write to track my emotional progress",
    "I journal to reflect on my life",
    "I find comfort in daily journaling",
    "I’ve noticed positive changes since I started journaling daily",
    "Writing has helped me clarify my goals",
    "I use journaling to better understand myself",
    "Journaling helps me release built-up emotions",
    "I write about how I feel every day",
    "I journal to track my mental and emotional growth",
    "Writing in my journal helps me stay mindful",
    "I document my thoughts daily to stay grounded",
    "Journaling allows me to work through my struggles",
    "I reflect on my personal challenges in my journal",
    "I write down my experiences to learn from them",
    "Journaling helps me create a roadmap for personal growth",
    "How can journaling help me reflect?",
    "I don’t know what to write in my journal.",
    "What are some journaling techniques?",
    "How do I get started with journaling?",
    "Can you recommend some self-reflection exercises?",
    "How do I use journaling to improve myself?",
    "What are some good daily journal entries?",
    "What should I write in my journal today?",
    "Can you give me journaling tips?",
    "I want to reflect on my feelings today in my journal.",
    "How do I keep a meaningful journal?",
    "Can you give me advice on how to journal regularly?",
    "What are some ways to get the most out of journaling?",
    "How do I start journaling for personal growth?",
    "I’m looking for prompts to improve self-reflection.",
    "What are some effective journaling practices?",
    "Can you suggest a journaling habit?",
    "What’s a good way to use journaling for mental health?",
    "How do I reflect on my day using my journal?",
    "I need help staying consistent with journaling."
  ],
"Depression_Talking": [
    "I feel so depressed.",
    "I think I’m depressed.",
    "What are the symptoms of depression?",
    "Can you help me with depression?",
    "How do I know if I have depression?",
    "What can I do to deal with depression?",
    "I don’t know how to handle my depression.",
    "I’m feeling really down.",
    "Is depression affecting me?",
    "I think I might be depressed.",
    "I feel like there’s no hope.",
    "I just feel empty inside.",
    "What should I do if I’m feeling depressed?",
    "How can I cope with depression?",
    "I feel numb and sad all the time.",
    "Is it normal to feel like this all the time?",
    "I’m struggling with depression.",
    "What can help me with depression?",
    "Can depression be treated?",
    "What are some ways to fight depression?",
    "How do I get out of this depressed state?",
    "How long does depression last?",
    "Is it okay to talk about depression?",
    "I don’t know how to cope with my depression.",
    "What should I do when I feel depressed?",
    "Can I beat depression on my own?",
    "I feel hopeless and sad."
  ],
"PTSD_Questions": [
    "What is PTSD?",
    "Can you explain PTSD?",
    "What are the signs of PTSD?",
    "How do I know if I have PTSD?",
    "What causes PTSD?",
    "What can help with PTSD?",
    "I think I might have PTSD.",
    "How can PTSD be treated?",
    "What should I do if I have PTSD?",
    "How do I cope with PTSD?",
    "What are the symptoms of PTSD?",
    "How does PTSD affect someone?",
    "Is PTSD curable?",
    "Can PTSD be managed?",
    "What are some common symptoms of PTSD?",
    "What should I do if I suspect PTSD?",
    "Can PTSD come from past trauma?",
    "What kind of therapy is best for PTSD?",
    "How do you overcome PTSD?",
    "Can PTSD affect relationships?",
    "What triggers PTSD?",
    "What is the best way to manage PTSD?",
    "How do you recognize PTSD?",
    "How do I heal from PTSD?",
    "What are the long-term effects of PTSD?",
    "How can PTSD impact daily life?"
  ],
"Loneliness_Talking": [
    "I feel so lonely.",
    "I have no one to talk to.",
    "I feel isolated from everyone.",
    "I just feel so alone.",
    "I think I’m really lonely.",
    "I feel disconnected from others.",
    "Loneliness is really hard for me.",
    "I wish I had someone to talk to.",
    "I feel like I don’t belong anywhere.",
    "I feel so isolated.",
    "It’s hard to make friends.",
    "I’m struggling with loneliness.",
    "I have no one around me.",
    "It’s like I’m invisible to everyone.",
    "I feel like nobody understands me.",
    "I feel left out all the time.",
    "I can’t shake this loneliness.",
    "I’m feeling disconnected from people.",
    "I don’t know how to deal with loneliness.",
    "I feel emotionally distant from everyone.",
    "I wish I didn’t feel this lonely.",
    "It feels like I have no support.",
    "I don’t know who to turn to for help.",
    "I feel like I have no friends.",
    "How do I overcome loneliness?",
    "Can loneliness affect your mental health?",
    "How can I make friends and stop feeling lonely?"
  ],
"Seeking_Support": [
    "I need help with my mental health.",
    "Can you help me with my feelings?",
    "How can I get mental health support?",
    "Who can I talk to about my mental health?",
    "I feel like I need someone to talk to.",
    "How do I get professional help?",
    "I need some support right now.",
    "Can you help me feel better?",
    "Where can I find mental health resources?",
    "I don’t know who to talk to for help.",
    "What kind of support do I need?",
    "How do I get a therapist?",
    "What can I do to improve my mental health?",
    "Where can I get mental health help?",
    "I feel like I need therapy.",
    "Can you recommend a counselor?",
    "How do I reach out for help?",
    "Where can I find mental health support?",
    "I need to speak with someone right now.",
    "Who can I talk to about my mental health issues?",
    "How can I improve my mental well-being?",
    "What do I do if I need emotional support?",
    "I’m looking for someone to talk to.",
    "How do I start therapy?",
    "Can I talk to someone right now about how I’m feeling?"
  ],
"Writing_Down_Thoughts": [
    "I write down my thoughts.",
    "I journal every day.",
    "How can journaling help me?",
    "What are the benefits of writing down my thoughts?",
    "What should I write about in my journal?",
    "How does journaling help with mental health?",
    "What’s the best way to start journaling?",
    "How can I get into the habit of journaling?",
    "What should I write in my thoughts journal?",
    "I feel better when I write my thoughts down.",
    "Why do I feel lighter after writing things down?",
    "Can journaling reduce stress?",
    "What type of journaling is best for mental health?",
    "How can journaling improve my emotional well-being?",
    "Is it okay to just write random thoughts in a journal?",
    "How does journaling help anxiety?",
    "What are some journaling prompts for mental health?",
    "Is journaling a good way to process emotions?",
    "Can journaling help with self-reflection?",
    "Should I write in my journal every day?",
    "How can I use journaling for mindfulness?",
    "What’s the relationship between journaling and mental clarity?",
    "Can journaling help with depression?",
    "How can journaling help with my mood?",
    "How do I make journaling part of my daily routine?",
    "What should I do when I’m stuck in my journal?",
    "What is the purpose of a mental health journal?",
    "How do I make journaling more effective?",
    "Can journaling help me figure out what I’m feeling?"
],
"No_Person_To_Talk_To": [
    "I don’t have anyone to talk to",
    "I feel like I have no one to talk to",
    "I don’t know who to talk to",
    "There’s no one I can talk to",
    "I’m feeling alone and have no one to talk to",
    "I wish I had someone to talk to",
    "I feel isolated with no one to talk to",
    "I have nobody to talk to about how I feel",
    "I don't know who to turn to for help",
    "I’m feeling really lonely right now",
    "I need someone to talk to but don't know who",
    "There’s no one who understands me",
    "I feel completely alone",
    "I have no support system right now",
    "I'm feeling disconnected from everyone",
    "I wish I could share my feelings with someone",
    "No one listens to me",
    "I feel like I’m invisible",
    "I feel like nobody cares about me",
    "I have no one to lean on right now",
    "I feel abandoned by the people around me",
    "I'm alone in my thoughts",
    "I have no friends to talk to",
    "I feel like I’m carrying everything by myself",
    "I don’t have anyone who gets what I’m going through",
    "I'm struggling to find someone who cares",
    "No one seems to understand me",
    "I feel like I'm talking to myself",
    "I'm afraid to open up to anyone",
    "I don't want to burden anyone with my problems",
    "I'm tired of being alone",
    "I just need someone who understands",
    "I have no support right now",
    "I don’t feel connected to anyone",
    "I feel completely alone in my struggles",
    "I’m not sure who to turn to for help",
    "Nobody is checking on me",
    "I don’t have anyone to help me through this",
    "I feel like I’m all by myself in this world",
    "I don’t know where to find someone to talk to",
    "I’ve tried talking to people, but they don’t understand",
    "I don't want to be a burden to anyone",
    "I wish I could open up but I don’t know how",
    "I'm feeling alone even though I’m surrounded by people",
    "I don’t have the courage to talk to anyone about this",
    "I wish someone would reach out to me",
    "I’ve isolated myself from everyone",
    "I feel like nobody cares enough to listen",
    "I’m dealing with everything alone",
    "I don’t know who to trust with my feelings",
    "I feel disconnected from everyone around me",
    "I don’t have anyone to help me with my emotional struggles",
    "I feel invisible to everyone in my life",
    "I need someone to talk to right now",
    "I don’t know where to turn for support",
    "I have no one to talk to who truly listens",
    "I feel emotionally alone",
    "There’s no one here for me when I need them",
    "I don't feel like I have anyone to rely on",
    "I’m overwhelmed by loneliness",
    "I feel isolated and invisible to the people around me",
    "I have nobody to share my feelings with",
    "I’ve been keeping everything inside",
    "I don't know how to reach out for help",
    "I don't know where to start to find support",
    "I feel empty inside without someone to talk to",
    "I don’t feel close to anyone in my life",
    "I’m longing for someone to talk to",
    "I'm emotionally drained because I'm all alone",
    "I wish someone would be there for me",
    "I feel disconnected from the people around me",
    "I’m afraid of opening up to anyone",
    "I'm not sure how to ask for help",
    "I wish I had a friend to confide in",
    "I'm too scared to talk to anyone about my struggles",
    "I feel distant from everyone around me",
    "I don’t feel like anyone cares enough to listen",
    "I feel completely on my own",
    "I feel so alone in my thoughts"
  ],
"Signs_Of_Depression": [
    "What are the signs of depression?",
    "How do I know if I’m depressed?",
    "What are symptoms of depression?",
    "How do I spot depression in myself?",
    "What should I look for to see if I have depression?",
    "How do you recognize depression?",
    "What are the first signs of depression?",
    "Can you tell if someone is depressed by their behavior?",
    "How do I know if I’m experiencing depression or just feeling down?",
    "What are the emotional signs of depression?",
    "How does depression affect daily life?",
    "How do you identify someone with depression?",
    "What physical symptoms come with depression?",
    "What’s the difference between sadness and depression?",
    "What are common indicators of depression?",
    "Is feeling tired a sign of depression?",
    "Can depression make you feel numb?",
    "Is not enjoying things a sign of depression?",
    "Can depression affect your appetite?",
    "How do you know if depression is affecting your work or school?",
    "What changes in behavior are related to depression?",
    "What signs show depression is getting worse?",
    "Is sleep disturbance a symptom of depression?",
    "What mental health conditions are linked with depression?",
    "Can someone feel depressed and still function normally?",
    "Is crying a lot a sign of depression?",
    "What’s the link between mood swings and depression?",
    "How do you deal with depression symptoms?",
    "Can depression be treated without medication?",
    "What are the signs of depression?",
    "How do I know if I have depression?",
    "What symptoms indicate depression?",
    "What are common signs of depression?",
    "How can I tell if I’m depressed?",
    "What does depression look like?",
    "How do I identify depression in myself?",
    "What are the red flags for depression?",
    "What should I look out for in depression?",
    "What are the early signs of depression?",
    "What are the emotional symptoms of depression?",
    "What physical symptoms could indicate depression?",
    "How do I recognize depression in my behavior?",
    "What are the warning signs of depression?",
    "How can I tell if I'm experiencing depression?",
    "What can cause depression?",
    "What does depression feel like?",
    "What are some of the effects of depression?",
    "How long should I feel sad before it's depression?",
    "What is a depressive episode?",
    "What are some common mental health signs of depression?",
    "How can I differentiate sadness from depression?",
    "What are the most noticeable signs of depression?",
    "How does depression affect your daily life?",
    "What are the warning signs of severe depression?",
    "What changes occur in a person with depression?",
    "What’s the difference between depression and just being sad?",
    "How does depression impact motivation?",
    "What changes in sleep patterns happen with depression?",
    "How does depression affect your ability to work?",
    "What is the emotional toll of depression?",
    "What are the stages of depression?",
    "What are the behavioral signs of depression?",
    "What should I do if I recognize depression signs?",
    "What mental changes happen with depression?",
    "What does a depressed person act like?",
    "What is the relationship between depression and stress?",
    "How does depression affect your concentration?",
    "What makes depression worse?",
    "What is the relationship between diet and depression?",
    "What role do genetics play in depression?",
    "What lifestyle changes can help with depression?",
    "How do you cope with depression?",
    "What are some treatments for depression?",
    "How do you know when it’s time to seek help for depression?",
    "How does depression affect family and relationships?",
    "What social signs should I look for in depression?",
    "How does depression affect your sense of self-worth?",
    "How long does depression last?",
    "What is the most effective way to manage depression?",
    "What are some long-term effects of depression?",
    "How do I know if depression is affecting my mental health?",
    "What are some signs of depression in teenagers?",
    "How does depression affect older adults?",
    "Can depression show up as irritability?",
    "How does depression impact physical health?",
    "How do I talk to someone about my depression?",
    "What makes depression harder to recognize?",
    "How do I manage my depression at home?",
    "What can you do to help someone with depression?",
    "How does depression affect your daily routine?",
    "Can depression lead to suicidal thoughts?",
    "What is the connection between depression and anxiety?",
    "How does depression affect your energy levels?",
    "What mental health treatments can help with depression?"
],
"Can_You_Help_Me": [
    "Can you help me?",
    "I need help, can you guide me?",
    "I feel lost, can you help?",
    "Can you support me?",
    "How do I get help for my mental health?",
    "What can I do if I need help?",
    "I don’t know where to start, can you help?",
    "How can I find someone to talk to?",
    "I feel stuck, can you give me advice?",
    "I need someone to talk to, can you listen?",
    "How do I seek help for my anxiety?",
    "Can you give me mental health resources?",
    "How do I ask for help when I’m struggling?",
    "I don’t feel supported, can you help?",
    "How can I find a therapist or counselor?",
    "Can you help me with self-care ideas?",
    "What should I do if I feel overwhelmed and alone?",
    "Where can I find professional help for my mental health?",
    "How do I talk to someone about my struggles?",
    "Can you recommend support groups?",
    "I don’t know how to start my healing journey, can you help?",
    "What are some immediate steps I can take for mental health support?",
    "Can you offer coping strategies for stress?",
    "How can I find mental health resources online?",
    "What should I do if I feel hopeless?",
    "Can you help me manage my mental health?",
    "Where can I talk to someone anonymously?",
    "How do I find a community to share my experiences?"
],
"Distancing_From_Toxic_Friends": [
    "I’m distancing myself from toxic friends.",
    "How do I cut ties with toxic people?",
    "What should I do if my friends are toxic?",
    "How can I stop being influenced by toxic friends?",
    "Is it okay to end friendships for my well-being?",
    "What are signs of toxic friendships?",
    "How do I protect my energy from negative people?",
    "Can I walk away from friendships that harm my mental health?",
    "How do I handle toxic people in my life?",
    "Is it normal to leave friends behind for personal growth?",
    "What is a toxic friend and how do I deal with them?",
    "How do I set boundaries with toxic people?",
    "Should I tell a toxic friend why I’m distancing myself?",
    "How do I manage guilt when distancing from toxic friends?",
    "What’s the best way to break up with a toxic friend?",
    "How can I prioritize my mental health over toxic friendships?",
    "Can toxic friends impact my self-esteem?",
    "What do I do if I feel drained by a friend?",
    "How can I deal with negative friendships without confrontation?",
    "Is it better to distance from toxic friends or confront them?",
    "What are healthy ways to end a toxic friendship?",
    "Can toxic friendships affect my growth?",
    "How do I know if I need to distance myself from someone?",
    "What happens when you distance yourself from toxic friends?",
    "Is it selfish to let go of toxic friends?",
    "How do I stay firm in my decision to distance from toxic friends?",
    "What is the long-term impact of staying in toxic friendships?",
    "How do I stop feeling bad about cutting off a friend?"
],
"Time_Management_and_Procrastination": [
    "I’m terrible at managing my time.",
    "I keep procrastinating, how can I stop?",
    "How do I get better at managing my day?",
    "What can I do to be more productive?",
    "How can I break free from procrastination?",
     "I can’t manage my time properly.",
  "I’m terrible at organizing my day.",
  "How can I get better at managing my time?",
  "I keep procrastinating because I can’t manage my time.",
  "I need help with time management, I can't get anything done.",
  "Why is it so hard for me to manage my time effectively?",
  "I struggle to balance everything because I can't plan my time well.",
  "I have too many things to do, but I can't figure out where to start.",
  "How do I stop procrastinating and start managing my time better?",
  "I need strategies to better manage my time between work and personal life.",
  "How do I improve my time management skills?",
  "I keep losing track of time and can't finish my tasks.",
  "I have a lot of tasks, but I don’t know how to organize them.",
  "How do I set priorities when everything seems urgent?",
  "What are the best time management techniques for someone like me?",
  "How do I avoid distractions and focus on managing my time better?",
  "I can never find time for the things that matter to me.",
  "How do I create a daily schedule to manage my tasks more effectively?",
  "I always feel like I'm behind because of poor time management.",
  "What’s a good way to set goals and manage my time better?",
    "What are some effective time management techniques?",
    "How do I avoid procrastination and stay focused?",
    "How can I stay on top of my schedule?",
    "What should I do if I keep putting things off?",
    "How do I manage my time better when I have a lot of tasks?",
    "What time management strategies work best?",
    "How do I stop wasting time?",
    "What are some easy steps to improve time management?",
    "How do I stick to a daily plan?",
    "How can I organize my day to be more productive?",
    "What are some tips for avoiding procrastination?",
    "How can I prioritize tasks effectively?",
    "How do I balance my personal and work life better?",
    "What are some productivity hacks to reduce procrastination?",
    "How can I avoid distractions during work?",
    "How do I make time for self-care and productivity?",
    "How can I stick to my schedule?",
    "How do I manage my tasks when I’m feeling overwhelmed?",
    "What are some daily habits that help with time management?",
    "How can I improve my focus and avoid distractions?",
    "What tools or apps can help with time management?",
    "How can I stay motivated to finish tasks?",
    "What should I do if I feel overwhelmed by my to-do list?"
],
"Anxiety_and_Depression": [
    "What is anxiety and depression?",
    "What’s the difference between anxiety and depression?",
    "How can anxiety affect mental health?",
    "What are the signs of anxiety?",
    "How do I know if I have anxiety or depression?",
    "Can depression cause anxiety?",
    "What causes anxiety and depression?",
    "How does anxiety feel?",
    "What is the impact of anxiety on daily life?",
    "What are the symptoms of depression?",
    "Can anxiety make you feel physically unwell?",
    "How do I deal with feelings of anxiety?",
    "What are the physical signs of depression?",
    "Can depression cause physical pain?",
    "What can I do if I feel anxious all the time?",
    "How does depression affect your mood?",
    "What is the best way to manage anxiety?",
    "How can I identify if I’m experiencing anxiety?",
    "What is the link between anxiety and depression?",
    "What are the long-term effects of untreated anxiety?",
    "How does anxiety affect your thoughts?",
    "Can someone have both anxiety and depression?",
    "What is the relationship between stress, anxiety, and depression?",
    "How do I distinguish between normal stress and anxiety?",
    "Can anxiety cause panic attacks?",
    "Is it common to feel anxious and sad at the same time?",
    "How does depression affect your energy levels?",
    "Can depression make you lose interest in life?",
    "What steps should I take if I’m feeling depressed and anxious?",
    "Is it possible to recover from anxiety and depression?",
    
], 
"Mental_Disorders": [
  "What are mental disorders?",
  "Can you explain what a mental disorder is?",
  "What types of mental disorders are there?",
  "How do mental health disorders affect daily life?",
  "What causes mental disorders?",
  "Are mental health disorders hereditary?",
  "What is the difference between a mental disorder and mental illness?",
  "How can mental disorders be treated?",
  "Is it normal to experience mental disorders?",
  "What are the signs of a mental disorder?",
  "How do I know if I have a mental disorder?",
  "What are the common mental disorders people face?",
  "Are mental disorders treatable?",
  "How can I seek help for a mental disorder?",
  "What are the most common types of mental health disorders?",
  "How can mental disorders affect someone's relationships?",
  "Can mental disorders be prevented?",
  "What is the role of therapy in treating mental disorders?",
  "What should you do if you suspect someone has a mental disorder?",
  "Are there medications for treating mental disorders?"
],
"Overwhelming_Depression_Feeling": [
  "Does feeling overwhelmed mean I am depressed?",
  "How do I know if my overwhelming feelings are a sign of depression?",
  "Is being overwhelmed the same as being depressed?",
  "Could my feelings of being overwhelmed be a sign of depression?",
  "How do I differentiate between feeling overwhelmed and depression?",
  "Can stress and feeling overwhelmed lead to depression?",
  "Does depression always come with feeling overwhelmed?",
  "Why do I feel overwhelmed, and is it related to depression?",
  "Is my stress level an indicator of depression?",
  "How can I know if I’m overwhelmed or truly depressed?",
  "Do feelings of being overwhelmed and depression always go together?",
  "How do I tell if my anxiety and overwhelm are linked to depression?",
  "What are the signs that my overwhelming feelings are depression?",
  "Is depression just feeling overwhelmed constantly?",
  "Could feeling overwhelmed mean I’m depressed and not aware of it?"
],
"Not_Depressed": [
  "I'm not depressed, just overwhelmed with everything.",
  "I don't think I’m depressed, I’m just struggling with time management.",
  "I'm not feeling depressed, I just can't seem to get organized.",
  "I'm not sure if I'm depressed, but I’m definitely struggling to manage my time.",
  "I don’t think I'm depressed, I just have too much on my plate.",
  "I don't feel depressed, I just can't handle everything at once.",
  "I don’t think I'm dealing with depression, it's just hard to manage my tasks.",
  "I don’t feel sad, I just don’t know how to manage everything I need to do.",
  "I'm not depressed, I just need help with organizing my life better.",
  "I don't think it's depression, I just struggle with balancing everything.",
  "I'm not feeling down, I just don't have enough time for everything.",
  "I'm not depressed, I'm just overwhelmed by my responsibilities.",
  "I don’t have symptoms of depression, I’m just dealing with a lot of stress.",
  "I'm not sad, I just don’t know how to manage my schedule.",
  "I’m not depressed, but I feel like I can't manage everything at once.",
  "I’m not feeling depressed, but my time management could definitely improve.",
  "I'm not dealing with depression, I’m just having a hard time organizing my day.",
  "I don't feel hopeless, I just can’t keep up with everything that’s happening.",
  "I’m not sad or depressed, but I do feel constantly overwhelmed.",
  "i am not depressed", "i no depressed", "i no dey depressed", "i am not actually depressed", "i am not feeling depressed"
],
"Academic_Balance_and_Time_Management": [
    "I want to learn how to manage my time well",
    "How can I set realistic academic goals without compromising my mental health?",
    "What role does time management play in balancing academics and mental well-being?",
    "How can I manage both my academic life and mental health effectively?",
    "How do you prioritize your academic workload without feeling overwhelmed?",
    "How can I balance my academic life, social life, and mental health?",
    "How do I stay productive and motivated in school when I'm tired?",
    "How can I make time for my social life and academics without sacrificing mental health?",
    "How do I manage stress with my academic commitments?",
    "What are the best strategies to balance exams and maintaining mental well-being?",
    "How do I avoid procrastination while balancing academic responsibilities?",
    "How can I overcome time management challenges in school?",
    "What are the most effective strategies for balancing academic stress and self-care?",
    "How can I handle multiple assignments and exams without burning out?",
    "What are some tips for balancing schoolwork with other extracurricular activities?",
    "How can I manage school stress while maintaining a healthy work-life balance?",
    "How do I stay focused on studies when I feel mentally drained?",
    "What are ways to manage academic pressure without negatively impacting my mental health?",
    "How can I keep my academic performance high while avoiding burnout?",
    "How do I deal with academic setbacks without letting them affect my mental health?",
    "How can I prioritize studying effectively while still caring for my mental well-being?",
    "How can I build resilience in managing both academics and emotional challenges?",
    "How do I cope with academic stress during exams without compromising my health?",
    "How do I balance school, work, and family responsibilities without feeling overwhelmed?",
    "How can I organize my study schedule to minimize stress and improve performance?",
    "How can I achieve a work-life balance as a student?",
    "What are some habits that help in managing schoolwork and reducing anxiety?",
    "How do I deal with academic demands without letting them affect my mood or energy?",
    "What are the best techniques to maintain mental well-being during exam periods?",
    "How can I stay motivated throughout the semester and prevent academic burnout?",
    "How can I manage my time well?",
    "How do I set realistic academic goals without compromising my mental health?",
    "What role does time management play in balancing academics and mental well-being?",
    "How can I manage both my academic life and mental health effectively?",
    "How do you prioritize your academic workload without feeling overwhelmed?",
    "How can I balance my academic life, social life, and mental health?",
    "How do I stay productive and motivated in school when I'm tired?",
    "How can I make time for my social life and academics without sacrificing mental health?",
    "How do I manage stress with my academic commitments?",
    "What are the best strategies to balance exams and maintaining mental well-being?",
    "How do I avoid procrastination while balancing academic responsibilities?",
    "How can I overcome time management challenges in school?",
    "What are the most effective strategies for balancing academic stress and self-care?",
    "How can I handle multiple assignments and exams without burning out?",
    "What are some tips for balancing schoolwork with other extracurricular activities?",
    "How can I manage school stress while maintaining a healthy work-life balance?",
    "How do I stay focused on studies when I feel mentally drained?",
    "What are ways to manage academic pressure without negatively impacting my mental health?",
    "How can I keep my academic performance high while avoiding burnout?",
    "How do I deal with academic setbacks without letting them affect my mental health?",
    "How can I prioritize studying effectively while still caring for my mental well-being?",
    "How can I build resilience in managing both academics and emotional challenges?",
    "How do I cope with academic stress during exams without compromising my health?",
    "How do I balance school, work, and family responsibilities without feeling overwhelmed?",
    "How can I organize my study schedule to minimize stress and improve performance?",
    "How can I achieve a work-life balance as a student?",
    "What are some habits that help in managing schoolwork and reducing anxiety?",
    "How do I deal with academic demands without letting them affect my mood or energy?",
    "What are the best techniques to maintain mental well-being during exam periods?",
    "How can I stay motivated throughout the semester and prevent academic burnout?"

],
"Mental_Health_and_Wellbeing": [
    "How can I balance mental health with academics?",
    "How do I handle stress and pressure while maintaining my mental health?",
    "What are some practical tips for managing mental health while in school?",
    "How do I prioritize my mental well-being while being a student?",
    "How can I reduce mental stress caused by academic challenges?",
    "What are some ways to avoid burnout as a student?",
    "How do I deal with anxiety during exams without letting it affect my studies?",
    "How can I maintain mental health while dealing with academic responsibilities?",
    "What are some ways to manage exam anxiety effectively?",
    "How can I balance mental health with academics?",
    "How do I handle stress and pressure while maintaining my mental health?",
    "What are some practical tips for managing mental health while in school?",
    "How do I prioritize my mental well-being while being a student?",
    "How can I reduce mental stress caused by academic challenges?",
    "What are some ways to avoid burnout as a student?",
    "How do I deal with anxiety during exams without letting it affect my studies?",
    "How can I maintain mental health while dealing with academic responsibilities?",
    "What are some ways to manage exam anxiety effectively?",
    "How can I prevent emotional exhaustion from schoolwork?",
    "How can I stay mentally strong while dealing with academic pressure?",
    "How do I manage my emotions while balancing school and life responsibilities?",
    "How can I cope with feeling overwhelmed during stressful academic periods?",
    "What should I do when I feel mentally drained by my academic work?",
    "How do I set boundaries to protect my mental health in school?",
    "How can I practice self-care during stressful academic seasons?",
    "How can I deal with school stress and still maintain a healthy mental state?",
    "What are effective strategies for dealing with mental exhaustion in school?",
    "How can I improve my mental well-being while being overwhelmed with academic tasks?",
    "How can I ensure my mental health doesn't suffer from academic workload?",
    "How do I stay positive and mentally healthy when facing academic challenges?",
    "How do I stay mentally stable while handling the stress of exams?",
    "What are some activities I can do to de-stress after a difficult academic period?",
    "How can I keep my mental health in check while managing school deadlines?",
    "How do I keep up with schoolwork and maintain my emotional balance?",
    "What are the best ways to handle mental stress without letting it affect my studies?",
    "How can I ensure my mental health is a priority while juggling school responsibilities?",
    "How do I stay mentally healthy when overwhelmed by academic tasks?",
    "What are some habits for maintaining good mental health while in school?",
    "How can I prevent emotional exhaustion from schoolwork?",
    "How can I stay mentally strong while dealing with academic pressure?",
    "How do I manage my emotions while balancing school and life responsibilities?",
    "How can I cope with feeling overwhelmed during stressful academic periods?",
    "What should I do when I feel mentally drained by my academic work?",
    "How do I set boundaries to protect my mental health in school?",
    "How can I practice self-care during stressful academic seasons?",
    "How can I deal with school stress and still maintain a healthy mental state?",
    "What are effective strategies for dealing with mental exhaustion in school?",
    "How can I improve my mental well-being while being overwhelmed with academic tasks?",
    "How can I ensure my mental health doesn't suffer from academic workload?",
    "How do I stay positive and mentally healthy when facing academic challenges?",
    "How do I stay mentally stable while handling the stress of exams?",
    "What are some activities I can do to de-stress after a difficult academic period?",
    "How can I keep my mental health in check while managing school deadlines?",
    "How do I keep up with schoolwork and maintain my emotional balance?",
    "What are the best ways to handle mental stress without letting it affect my studies?",
    "How can I ensure my mental health is a priority while juggling school responsibilities?",
    "How do I stay mentally healthy when overwhelmed by academic tasks?",
    "What are some habits for maintaining good mental health while in school?"
],
"Social_Life_and_Academic_Balance": [
    "How can I create meaningful social connections while maintaining a high GPA?",
    "How do I balance social events and academic responsibilities?",
    "How do I attend social events and still maintain a strong academic performance?",
    "How can I prioritize my academic work while making time for socializing?",
    "What are ways to socialize while managing academic pressure?",
    "How do I balance my social life and academic life as a student?",
    "How can I maintain friendships while focusing on schoolwork?",
    "How do I find time for my friends without sacrificing my grades?",
    "How can I create a social life outside of my academic commitments?",
    "How can I build friendships while keeping my grades up?",
    "How do I navigate the social expectations of university while managing my studies?",
    "How do I find a balance between attending social events and studying?",
    "What are ways to stay connected with friends without compromising my academic goals?",
     "How can I create meaningful social connections while maintaining a high GPA?",
    "How do I balance social events and academic responsibilities?",
    "How do I attend social events and still maintain a strong academic performance?",
    "How can I prioritize my academic work while making time for socializing?",
    "What are ways to socialize while managing academic pressure?",
    "How do I balance my social life and academic life as a student?",
    "How can I maintain friendships while focusing on schoolwork?",
    "How do I find time for my friends without sacrificing my grades?",
    "How can I create a social life outside of my academic commitments?",
    "How can I build friendships while keeping my grades up?",
    "How do I navigate the social expectations of university while managing my studies?",
    "How do I find a balance between attending social events and studying?",
    "What are ways to stay connected with friends without compromising my academic goals?",
    "How do I handle FOMO (fear of missing out) while focusing on my academic work?",
    "How do I create opportunities to socialize without neglecting my studies?",
    "How do I avoid isolating myself while focusing on academic success?",
    "How do I strike a balance between social commitments and academic obligations?",
    "How can I stay socially active while still being productive with my academic tasks?",
    "How do I manage social pressures and academic challenges at the same time?",
    "How can I avoid burnout while balancing social life and academics?",
    "How do I keep my social life balanced while managing academic stress?",
    "How do I incorporate social activities into my academic schedule without overloading myself?",
    "How do I participate in extracurricular activities without losing focus on my academics?",
    "How can I balance relationships, studies, and self-care in college?",
    "How do I deal with social anxiety while keeping up with academics?",
    "How can I socialize without feeling guilty about my academic commitments?",
    "How do I avoid the trap of neglecting social interactions due to academic stress?",
    "How do I prioritize social time to improve my well-being while still achieving academically?",
    "How can I use social activities to help reduce academic stress and improve my focus?",
    "How do I handle FOMO (fear of missing out) while focusing on my academic work?",
    "How do I create opportunities to socialize without neglecting my studies?",
    "How do I avoid isolating myself while focusing on academic success?",
    "How do I strike a balance between social commitments and academic obligations?",
    "How can I stay socially active while still being productive with my academic tasks?",
    "How do I manage social pressures and academic challenges at the same time?",
    "How can I avoid burnout while balancing social life and academics?",
    "How do I keep my social life balanced while managing academic stress?",
    "How do I incorporate social activities into my academic schedule without overloading myself?",
    "How do I participate in extracurricular activities without losing focus on my academics?",
    "How can I balance relationships, studies, and self-care in college?",
    "How do I deal with social anxiety while keeping up with academics?",
    "How can I socialize without feeling guilty about my academic commitments?",
    "How do I avoid the trap of neglecting social interactions due to academic stress?",
    "How do I prioritize social time to improve my well-being while still achieving academically?",
    "How can I use social activities to help reduce academic stress and improve my focus?"
],
"Spiritual_and_Academic_Balance": [
    "How can I put God first in my academic life?",
    "How do I balance spirituality and academics?",
    "What role does spirituality play in achieving academic success?",
    "How can I incorporate my spiritual practices into my daily academic routine?",
    "How do I prioritize my spiritual well-being while maintaining academic responsibilities?",
    "How can I integrate prayer and study time effectively?",
    "What are some ways to stay spiritually grounded while pursuing academic goals?",
    "How do I deal with academic stress while relying on my faith?",
    "How can my spiritual beliefs help me cope with academic challenges?",
    "How do I maintain a strong spiritual life while dealing with the pressures of school?",
    "What are some strategies for balancing my spiritual life and academic pursuits?",
    "How do I stay focused on my spiritual life without neglecting my academic goals?",
    "How can I rely on my faith to overcome academic struggles?",
    "How do I find peace through my spiritual practices while facing academic deadlines?",
    "How do I navigate academic stress while staying connected to my spirituality?",
    "How can I develop a consistent spiritual routine that complements my academic schedule?",
    "How do I stay spiritually healthy while juggling schoolwork?",
    "How can spirituality enhance my ability to succeed academically?",
    "How can I integrate mindfulness and meditation into my academic life?",
    "How do I maintain spiritual well-being in a demanding academic environment?",
    "How can I use my spiritual practices to overcome feelings of academic overwhelm?",
    "How do I keep my faith strong while working toward academic success?",
    "How can I pray effectively for wisdom and guidance in my studies?",
    "How do I balance academic responsibilities with church or spiritual activities?",
    "How can I strengthen my spiritual life during stressful academic periods?",
    "How do I integrate my faith into my approach to studying?",
    "How do I cultivate spiritual growth while managing academic pressure?",
     "How can I put God first in my academic life?",
    "How do I balance spirituality and academics?",
    "What role does spirituality play in achieving academic success?",
    "How can I incorporate my spiritual practices into my daily academic routine?",
    "How do I prioritize my spiritual well-being while maintaining academic responsibilities?",
    "How can I integrate prayer and study time effectively?",
    "What are some ways to stay spiritually grounded while pursuing academic goals?",
    "How do I deal with academic stress while relying on my faith?",
    "How can my spiritual beliefs help me cope with academic challenges?",
    "How do I maintain a strong spiritual life while dealing with the pressures of school?",
    "What are some strategies for balancing my spiritual life and academic pursuits?",
    "How do I stay focused on my spiritual life without neglecting my academic goals?",
    "How can I rely on my faith to overcome academic struggles?",
    "How do I find peace through my spiritual practices while facing academic deadlines?",
    "How do I navigate academic stress while staying connected to my spirituality?",
    "How can I develop a consistent spiritual routine that complements my academic schedule?",
    "How do I stay spiritually healthy while juggling schoolwork?",
    "How can spirituality enhance my ability to succeed academically?",
    "How can I integrate mindfulness and meditation into my academic life?",
    "How do I maintain spiritual well-being in a demanding academic environment?",
    "How can I use my spiritual practices to overcome feelings of academic overwhelm?",
    "How do I keep my faith strong while working toward academic success?",
    "How can I pray effectively for wisdom and guidance in my studies?",
    "How do I balance academic responsibilities with church or spiritual activities?",
    "How can I strengthen my spiritual life during stressful academic periods?",
    "How do I integrate my faith into my approach to studying?",
    "How do I cultivate spiritual growth while managing academic pressure?",
],
"Coping_Strategies_for_Academic_and_Mental_Health": [
    "How can I handle overwhelming academic pressure without affecting my mental health?",
    "What are some coping strategies for dealing with exam stress?",
    "How do I manage my mental health while preparing for major exams?",
    "What are some ways to avoid burnout during high-pressure academic periods?",
    "How do I deal with feelings of inadequacy during academic challenges?",
    "How do I stay motivated when I feel overwhelmed by schoolwork?",
    "What are some techniques for staying calm during stressful academic moments?",
    "How can I build resilience against academic stress?",
     "How can I handle overwhelming academic pressure without affecting my mental health?",
    "What are some coping strategies for dealing with exam stress?",
    "How do I manage my mental health while preparing for major exams?",
    "What are some ways to avoid burnout during high-pressure academic periods?",
    "How do I deal with feelings of inadequacy during academic challenges?",
    "How do I stay motivated when I feel overwhelmed by schoolwork?",
    "What are some techniques for staying calm during stressful academic moments?",
    "How can I build resilience against academic stress?",
    "What are the best ways to cope with academic failures and setbacks?",
    "How do I maintain emotional stability during academic struggles?",
    "How do I avoid emotional burnout during the school year?",
    "How do I practice self-compassion when I don't perform well academically?",
    "What are the best ways to cope with academic pressure during the final exam period?",
    "How can I maintain mental clarity and focus despite academic challenges?",
    "How do I stay optimistic despite academic obstacles?",
    "What are the most effective coping mechanisms for academic anxiety?",
    "How do I handle perfectionism while pursuing academic success?",
    "What are some ways to stay positive during the most stressful academic seasons?",
    "How do I manage my emotions when I feel mentally and physically drained by schoolwork?",
    "How do I practice mindfulness to reduce stress during academic stress?",
    "How do I avoid negative thought patterns that affect my academic performance?",
    "How do I stay resilient when academic challenges feel overwhelming?",
    "What are some coping strategies for dealing with the mental demands of academic life?",
    "How do I keep up with schoolwork without sacrificing my mental health?",
    "What are some healthy coping mechanisms for managing academic stress?",
    "How can I maintain balance when facing academic challenges and emotional stress?",
    "What are the best ways to cope with academic failures and setbacks?",
    "How do I maintain emotional stability during academic struggles?",
    "How do I avoid emotional burnout during the school year?",
    "How do I practice self-compassion when I don't perform well academically?",
    "What are the best ways to cope with academic pressure during the final exam period?",
    "How can I maintain mental clarity and focus despite academic challenges?",
    "How do I stay optimistic despite academic obstacles?",
    "What are the most effective coping mechanisms for academic anxiety?",
    "How do I handle perfectionism while pursuing academic success?",
    "What are some ways to stay positive during the most stressful academic seasons?",
    "How do I manage my emotions when I feel mentally and physically drained by schoolwork?",
    "How do I practice mindfulness to reduce stress during academic stress?",
    "How do I avoid negative thought patterns that affect my academic performance?",
    "How do I stay resilient when academic challenges feel overwhelming?",
    "What are some coping strategies for dealing with the mental demands of academic life?",
    "How do I keep up with schoolwork without sacrificing my mental health?",
    "What are some healthy coping mechanisms for managing academic stress?",
    "How can I maintain balance when facing academic challenges and emotional stress?"
],



     }

    def load_or_train_model(self):
        model_path = 'model.pkl'
        # Check if model already exists
        if os.path.exists(model_path):
            try:
                with open(model_path, 'rb') as f:
                    # Change this line to unpack both model and vectorizer
                    self.model, self.vectorizer = pickle.load(f)
            except (FileNotFoundError, pickle.UnpicklingError) as e:
                print(f"Error loading model: {e}")
                self.train_model()  # Train the model if loading fails
        else:
            self.train_model()
            
    def train_model(self):
        all_texts = []
        all_labels = []
        for intent, phrases in self.intents.items():
            for phrase in phrases:
                all_texts.append(phrase.lower())
                all_labels.append(intent)
        
        # Vectorization and Training
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(all_texts)
        model = LogisticRegression()
        model.fit(X, all_labels)
        
        self.model = model
        self.vectorizer = vectorizer

        # Save the model and vectorizer
        with open('model.pkl', 'wb') as f:
            pickle.dump((self.model, self.vectorizer), f)

    def post(self, request):
        print(request.headers)  # Log all headers
        try:
            # 1. Check authentication
            if not request.user.is_authenticated:
                return Response({"error": "User not authenticated"}, status=401)

            # 1. Get initial input
            user_message = request.data.get('message', '')
            
            if not user_message:
                return Response({"error": "No message provided."}, status=400)

            # 2. Preprocess the input
            if NLTK_DATA_AVAILABLE:
                stop_words = set(stopwords.words('english'))
            else:
                stop_words = set()
                
            tokens = word_tokenize(user_message.lower())
            filtered_tokens = [word for word in tokens if word.isalnum() and word not in stop_words]
            
            # 3. Get ML prediction
            user_input_vectorized = self.vectorizer.transform([' '.join(filtered_tokens)])
            predicted_intent_ml = self.model.predict(user_input_vectorized)[0]

            # 4. Get frequency-based prediction
            word_freq = Counter(filtered_tokens)
            intent_scores = {}
            
            for intent, phrases in self.intents.items():
                intent_score = 0
                for phrase in phrases:
                    phrase_tokens = word_tokenize(phrase.lower())
                    for token in phrase_tokens:
                        if token in word_freq:
                            intent_score += word_freq[token]
                intent_scores[intent] = intent_score

            # 5. Combine predictions
            predicted_intent_freq = max(intent_scores, key=intent_scores.get)
            predicted_intent = predicted_intent_freq if intent_scores[predicted_intent_freq] > 0 else predicted_intent_ml

            # 6. Get response based on intent
            responses = {
                "greeting": [
    "Hello! I'm SereniAI, your mental health support companion. How are you feeling today?",
    "Hi there! I'm here to listen and support you. Would you like to talk about what's on your mind?",
    "Welcome! I'm SereniAI, a safe space for you to share your thoughts and feelings. How can I help you today?",
    "Hello! I'm your mental wellness companion SereniAI. What brings you here today?",
    "Hi! I'm SereniAI, and I'm here to support you through anything you're experiencing. How are you doing?",
    "Greetings! I'm SereniAI, offering you a space of understanding and support. Would you like to share what's on your mind?",
    "Welcome to our conversation! I'm SereniAI, here to listen and provide support. How's your day going?",
    "Hello there! Thank you for reaching out to SereniAI. How can I make this space more comfortable for you?",
    "Hi! I'm your AI companion SereniAI. I'm here to listen without judgment. What would you like to discuss?",
    "Welcome! This is SereniAI, creating a safe environment for you to express yourself. How are you feeling right now?",
    "Hello! I'm SereniAI, ready to support your emotional well-being. What's been on your mind lately?",
    "Hi there! SereniAI here, offering a space where you can feel heard and understood. How can I help you today?",
    "Greetings! I'm your supportive companion SereniAI. What would you like to talk about?",
    "Welcome! I'm SereniAI, here to provide emotional support and understanding. How's everything going?",
    "Hello! This is your mental health ally SereniAI. How can I support you today?",
    "Hi! SereniAI here, ready to listen and provide a caring presence. What's on your heart?",
    "Welcome to our safe space! I'm SereniAI, here to support your journey. How are you feeling at this moment?",
    "Hello there! I'm SereniAI, your emotional support companion. What would you like to explore today?",
    "Hi! Thank you for connecting with SereniAI. I'm here to help you process your thoughts. How's your day been?",
    "Greetings! This is SereniAI, offering you understanding and support. What's been happening in your world?",
    "Welcome! I'm your companion SereniAI, here to listen and support. How can I help you feel more at ease?",
    "Hello! SereniAI present and ready to provide emotional support. What's on your mind today?",
    "Hi there! I'm SereniAI, creating a judgment-free zone for you. Would you like to share what brings you here?",
    "Greetings! Thank you for reaching out to SereniAI. How can I make this conversation helpful for you?",
    "Welcome! I'm your supportive AI companion SereniAI. What would you like to focus on today?",
    "Hello! This is SereniAI, here to provide a listening ear. How are you doing right now?",
    "Hi! I'm SereniAI, your mental wellness partner. What's been weighing on your mind?",
    "Greetings! SereniAI here, ready to support your emotional journey. How can I help you today?",
    "Welcome to our conversation space! I'm SereniAI, offering support and understanding. What brings you here?",
    "Hello there! I'm your AI companion SereniAI. How can I support you through your current experiences?",
    "Hi! This is SereniAI, providing a safe harbor for your thoughts. How are you feeling today?",
    "Welcome! I'm SereniAI, here to listen and understand. What would you like to discuss?",
    "Greetings! Thank you for sharing this space with SereniAI. How can I support you best?",
    "Hello! I'm your emotional support companion SereniAI. What's been going on in your life?",
    "Hi there! SereniAI ready to provide care and understanding. How are you doing today?",
    "Welcome! This is SereniAI, offering a comfortable space for conversation. What's on your mind?",
    "Hello! I'm SereniAI, your mental health support partner. How can I help you process your feelings?",
    "Hi! SereniAI here, creating a safe environment for expression. Would you like to share what's happening?",
    "Greetings! I'm your AI companion SereniAI. How can I make this space more supportive for you?",
    "Welcome to our safe haven! I'm SereniAI, here to listen and care. What brings you here today?",
    "Hello there! Thank you for choosing SereniAI. How can I help you feel more heard?",
    "Hi! I'm your dedicated support companion SereniAI. What would you like to explore together?",
    "Welcome! SereniAI present and ready to support your journey. How are you feeling right now?",
    "Greetings! This is SereniAI, offering understanding and companionship. What's been on your heart?",
    "Hello! I'm SereniAI, here to provide emotional guidance. How can I support you today?",
    "Hi there! I'm your mental wellness companion SereniAI. Would you like to share what's happening?",
    "Welcome! SereniAI here, creating a space for open dialogue. How's everything going?",
    "Hello! Thank you for connecting with SereniAI. What would you like to talk about?",
    "Hi! I'm SereniAI, your supportive presence. How can I help you navigate your feelings?",
    "Greetings! This is SereniAI, offering a judgment-free environment. What's on your mind?",
    "Welcome to our conversation! I'm SereniAI, here to support and understand. How are you doing?",
    "Hello there! SereniAI ready to provide emotional support. What brings you here today?",
    "Hi! I'm your AI companion SereniAI. How can I help you feel more supported?",
    "Welcome! This is SereniAI, creating a safe space for sharing. Would you like to talk about what's happening?",
    "Greetings! Thank you for reaching out to SereniAI. How can I be most helpful today?",
    "Hello! I'm SereniAI, your mental health ally. What would you like to focus on?",
    "Hi there! SereniAI here, offering understanding and support. How's your day going?",
    "Welcome! I'm your emotional support companion SereniAI. What's been on your mind lately?",
    "Hello! This is SereniAI, providing a caring presence. How can I support you today?",
    "Hi! Thank you for choosing SereniAI. Would you like to share what brings you here?",
    "Greetings! I'm your AI companion SereniAI. How can I help you process your thoughts?",
    "Welcome to our safe space! SereniAI here to listen and support. What's happening in your world?",
    "Hello there! I'm SereniAI, your mental wellness partner. How are you feeling right now?",
    "Hi! This is SereniAI, offering a judgment-free zone. What would you like to discuss?",
    "Welcome! I'm your supportive companion SereniAI. How can I make this space more comfortable?",
    "Greetings! SereniAI present and ready to help. What's been weighing on your mind?",
    "Hello! Thank you for connecting with SereniAI. How can I support your emotional well-being?",
    "Hi there! I'm your dedicated AI companion SereniAI. Would you like to share what's happening?",
    "Welcome! This is SereniAI, creating a space for healing. How's everything going?",
    "Hello! I'm SereniAI, here to provide understanding and support. What brings you here today?",
    "Hi! SereniAI ready to listen and care. How can I help you navigate your feelings?",
    "Greetings! Thank you for reaching out to SereniAI. What would you like to explore together?",
    "Welcome to our conversation space! I'm SereniAI, offering support and guidance. How are you doing?",
    "Hello there! This is SereniAI, your emotional support ally. What's been on your heart?",
    "Hi! I'm your mental health companion SereniAI. How can I make this space most helpful for you?",
    "Welcome! SereniAI here, providing a safe harbor for your thoughts. Would you like to share what's happening?",
    "Greetings! I'm your supportive AI presence SereniAI. What's been going on in your life?",
    "Hello! This is SereniAI, offering understanding and companionship. How are you feeling today?",
    "Hi there! Thank you for choosing SereniAI. What would you like to focus on in our conversation?",
    "Welcome! I'm your dedicated support companion SereniAI. How can I help you feel more heard?",
    "Hello! SereniAI present and ready to support your journey. What brings you here?",
    "Hi! This is SereniAI, creating a safe environment for expression. How's your day been?",
    "Greetings! I'm your AI companion SereniAI. Would you like to share what's on your mind?",
    "Welcome to our safe haven! SereniAI here to listen and understand. How can I support you today?",
    "Hello there! Thank you for connecting with SereniAI. What's been happening in your world?",
    "Hi! I'm your mental wellness partner SereniAI. How are you feeling right now?",
    "Welcome! This is SereniAI, offering a space for open dialogue. What would you like to discuss?",
    "Greetings! SereniAI ready to provide emotional support. How can I make this conversation helpful?"
  ],
        "greet": [
    "Hello! I'm SereniAI, your mental health support companion. How are you feeling today?",
    "Hi there! I'm here to listen and support you. Would you like to talk about what's on your mind?",
    "Welcome! I'm SereniAI, a safe space for you to share your thoughts and feelings. How can I help you today?",
    "Hello! I'm your mental wellness companion SereniAI. What brings you here today?",
    "Hi! I'm SereniAI, and I'm here to support you through anything you're experiencing. How are you doing?",
    "Greetings! I'm SereniAI, offering you a space of understanding and support. Would you like to share what's on your mind?",
    "Welcome to our conversation! I'm SereniAI, here to listen and provide support. How's your day going?",
    "Hello there! Thank you for reaching out to SereniAI. How can I make this space more comfortable for you?",
    "Hi! I'm your AI companion SereniAI. I'm here to listen without judgment. What would you like to discuss?",
    "Welcome! This is SereniAI, creating a safe environment for you to express yourself. How are you feeling right now?",
    "Hello! I'm SereniAI, ready to support your emotional well-being. What's been on your mind lately?",
    "Hi there! SereniAI here, offering a space where you can feel heard and understood. How can I help you today?",
    "Greetings! I'm your supportive companion SereniAI. What would you like to talk about?",
    "Welcome! I'm SereniAI, here to provide emotional support and understanding. How's everything going?",
    "Hello! This is your mental health ally SereniAI. How can I support you today?",
    "Hi! SereniAI here, ready to listen and provide a caring presence. What's on your heart?",
    "Welcome to our safe space! I'm SereniAI, here to support your journey. How are you feeling at this moment?",
    "Hello there! I'm SereniAI, your emotional support companion. What would you like to explore today?",
    "Hi! Thank you for connecting with SereniAI. I'm here to help you process your thoughts. How's your day been?",
    "Greetings! This is SereniAI, offering you understanding and support. What's been happening in your world?",
    "Welcome! I'm your companion SereniAI, here to listen and support. How can I help you feel more at ease?",
    "Hello! SereniAI present and ready to provide emotional support. What's on your mind today?",
    "Hi there! I'm SereniAI, creating a judgment-free zone for you. Would you like to share what brings you here?",
    "Greetings! Thank you for reaching out to SereniAI. How can I make this conversation helpful for you?",
    "Welcome! I'm your supportive AI companion SereniAI. What would you like to focus on today?",
    "Hello! This is SereniAI, here to provide a listening ear. How are you doing right now?",
    "Hi! I'm SereniAI, your mental wellness partner. What's been weighing on your mind?",
    "Greetings! SereniAI here, ready to support your emotional journey. How can I help you today?",
    "Welcome to our conversation space! I'm SereniAI, offering support and understanding. What brings you here?",
    "Hello there! I'm your AI companion SereniAI. How can I support you through your current experiences?",
    "Hi! This is SereniAI, providing a safe harbor for your thoughts. How are you feeling today?",
    "Welcome! I'm SereniAI, here to listen and understand. What would you like to discuss?",
    "Greetings! Thank you for sharing this space with SereniAI. How can I support you best?",
    "Hello! I'm your emotional support companion SereniAI. What's been going on in your life?",
    "Hi there! SereniAI ready to provide care and understanding. How are you doing today?",
    "Welcome! This is SereniAI, offering a comfortable space for conversation. What's on your mind?",
    "Hello! I'm SereniAI, your mental health support partner. How can I help you process your feelings?",
    "Hi! SereniAI here, creating a safe environment for expression. Would you like to share what's happening?",
    "Greetings! I'm your AI companion SereniAI. How can I make this space more supportive for you?",
    "Welcome to our safe haven! I'm SereniAI, here to listen and care. What brings you here today?",
    "Hello there! Thank you for choosing SereniAI. How can I help you feel more heard?",
    "Hi! I'm your dedicated support companion SereniAI. What would you like to explore together?",
    "Welcome! SereniAI present and ready to support your journey. How are you feeling right now?",
    "Greetings! This is SereniAI, offering understanding and companionship. What's been on your heart?",
    "Hello! I'm SereniAI, here to provide emotional guidance. How can I support you today?",
    "Hi there! I'm your mental wellness companion SereniAI. Would you like to share what's happening?",
    "Welcome! SereniAI here, creating a space for open dialogue. How's everything going?",
    "Hello! Thank you for connecting with SereniAI. What would you like to talk about?",
    "Hi! I'm SereniAI, your supportive presence. How can I help you navigate your feelings?",
    "Greetings! This is SereniAI, offering a judgment-free environment. What's on your mind?",
    "Welcome to our conversation! I'm SereniAI, here to support and understand. How are you doing?",
    "Hello there! SereniAI ready to provide emotional support. What brings you here today?",
    "Hi! I'm your AI companion SereniAI. How can I help you feel more supported?",
    "Welcome! This is SereniAI, creating a safe space for sharing. Would you like to talk about what's happening?",
    "Greetings! Thank you for reaching out to SereniAI. How can I be most helpful today?",
    "Hello! I'm SereniAI, your mental health ally. What would you like to focus on?",
    "Hi there! SereniAI here, offering understanding and support. How's your day going?",
    "Welcome! I'm your emotional support companion SereniAI. What's been on your mind lately?",
    "Hello! This is SereniAI, providing a caring presence. How can I support you today?",
    "Hi! Thank you for choosing SereniAI. Would you like to share what brings you here?",
    "Greetings! I'm your AI companion SereniAI. How can I help you process your thoughts?",
    "Welcome to our safe space! SereniAI here to listen and support. What's happening in your world?",
    "Hello there! I'm SereniAI, your mental wellness partner. How are you feeling right now?",
    "Hi! This is SereniAI, offering a judgment-free zone. What would you like to discuss?",
    "Welcome! I'm your supportive companion SereniAI. How can I make this space more comfortable?",
    "Greetings! SereniAI present and ready to help. What's been weighing on your mind?",
    "Hello! Thank you for connecting with SereniAI. How can I support your emotional well-being?",
    "Hi there! I'm your dedicated AI companion SereniAI. Would you like to share what's happening?",
    "Welcome! This is SereniAI, creating a space for healing. How's everything going?",
    "Hello! I'm SereniAI, here to provide understanding and support. What brings you here today?",
    "Hi! SereniAI ready to listen and care. How can I help you navigate your feelings?",
    "Greetings! Thank you for reaching out to SereniAI. What would you like to explore together?",
    "Welcome to our conversation space! I'm SereniAI, offering support and guidance. How are you doing?",
    "Hello there! This is SereniAI, your emotional support ally. What's been on your heart?",
    "Hi! I'm your mental health companion SereniAI. How can I make this space most helpful for you?",
    "Welcome! SereniAI here, providing a safe harbor for your thoughts. Would you like to share what's happening?",
    "Greetings! I'm your supportive AI presence SereniAI. What's been going on in your life?",
    "Hello! This is SereniAI, offering understanding and companionship. How are you feeling today?",
    "Hi there! Thank you for choosing SereniAI. What would you like to focus on in our conversation?",
    "Welcome! I'm your dedicated support companion SereniAI. How can I help you feel more heard?",
    "Hello! SereniAI present and ready to support your journey. What brings you here?",
    "Hi! This is SereniAI, creating a safe environment for expression. How's your day been?",
    "Greetings! I'm your AI companion SereniAI. Would you like to share what's on your mind?",
    "Welcome to our safe haven! SereniAI here to listen and understand. How can I support you today?",
    "Hello there! Thank you for connecting with SereniAI. What's been happening in your world?",
    "Hi! I'm your mental wellness partner SereniAI. How are you feeling right now?",
    "Welcome! This is SereniAI, offering a space for open dialogue. What would you like to discuss?",
    "Greetings! SereniAI ready to provide emotional support. How can I make this conversation helpful?"
  ],

"Work_Study_Impact": [
    "I understand you're experiencing anxiety related to your work/studies. Let's explore how this is affecting you. Work and academic pressures can be particularly challenging because they often involve performance expectations, deadlines, and evaluation from others. First, let's identify specific situations that trigger your anxiety - whether it's presentations, deadlines, team interactions, or test-taking. Then we can develop targeted strategies to help you manage these situations while maintaining your performance. Remember, many successful professionals and students deal with similar challenges, and there are effective ways to handle this.",

    "Let's take a moment to understand how anxiety is impacting your work or academic life. Many people find that anxiety affects their concentration, memory, and overall performance. Could you describe what you're experiencing? Are you noticing specific patterns, like increased anxiety before certain tasks or in particular situations? Understanding these patterns can help us develop effective coping strategies that work within your professional or academic environment. We can explore techniques that not only help manage anxiety but might even enhance your performance.",

    "I hear that you're struggling with anxiety in your work/study environment. This is a common but challenging experience that deserves careful attention. Let's start by creating a safe space to explore how anxiety is manifesting in your professional or academic life. Are you experiencing physical symptoms like racing thoughts during meetings or exams? Or perhaps you're finding it difficult to concentrate on tasks? Together, we can develop strategies that help you maintain your performance while managing anxiety effectively. Many people find that with the right tools, they can not only cope with work/study anxiety but actually thrive.",

    "Work and academic anxiety can be particularly challenging because these environments often demand our best performance. Let's work together to understand your specific situation. What aspects of your work or studies trigger the most anxiety? Is it specific tasks, interactions with colleagues/peers, or perhaps performance evaluations? Once we identify these triggers, we can develop personalized strategies to help you manage anxiety while maintaining your effectiveness. Remember, experiencing anxiety doesn't diminish your capabilities or potential for success.",

    "Thank you for sharing your concerns about anxiety affecting your work or studies. This is an important area to address, as our professional and academic lives often require sustained focus and performance. Let's start by understanding your specific challenges. Are you finding it difficult to concentrate? Feeling overwhelmed by deadlines? Experiencing anxiety during presentations or exams? Together, we can develop practical strategies that fit into your daily routine and help you manage anxiety while maintaining your professional or academic performance. Many successful individuals have learned to work with their anxiety rather than against it."
  ],
"Behavioral_Responses": [
    "It's natural to want to avoid anxiety-inducing situations, but facing them gradually can help you build resilience. \n\nStep 1: Start by identifying the specific situations that cause you anxiety. \nStep 2: Break these situations down into smaller, manageable steps. \nStep 3: Gradually expose yourself to these situations, starting with the least anxiety-provoking scenario. \n\nBy using Serenimind's gradual exposure techniques, you can work through these steps at your own pace, gradually reducing your anxiety and building confidence.",
    
    "Many people develop coping behaviors to handle anxiety, such as avoiding certain places or situations. \n\nStep 1: Reflect on and write down the situations or habits you tend to avoid due to anxiety. \nStep 2: Identify which of these habits are limiting your daily life. \nStep 3: Work on replacing avoidance behaviors with healthier coping mechanisms, such as deep breathing or mindfulness. \n\nSerenimind offers exercises that can help you replace these avoidance habits, making you feel more in control.",
    
    "Nervous habits like fidgeting or nail-biting are common signs of anxiety. \n\nStep 1: Observe your anxious behaviors and identify the triggers that cause them. \nStep 2: Replace these habits with healthier responses, like squeezing a stress ball, deep breathing, or progressive muscle relaxation. \nStep 3: Consistently practice these new behaviors whenever you feel anxious. \n\nSerenimind can help you track your progress and remind you to practice these new behaviors to reinforce positive changes.",
    
    "Avoiding anxiety-provoking situations is common, but over time, it can reinforce the fear. \n\nStep 1: Write down the situations that you tend to avoid and rank them based on how overwhelming they are. \nStep 2: Start facing these situations one by one, beginning with the least overwhelming. \nStep 3: As you gradually expose yourself to these situations, celebrate your progress and reflect on how you handled each one. \n\nSerenimind provides support through structured guidance and regular check-ins to help you feel confident throughout this process.",
    
    "When you feel stressed, your body may react in ways that you don't fully control, such as rapid heartbeat or shallow breathing. \n\nStep 1: Pay attention to your body’s stress signals, like a fast heartbeat or tight muscles. \nStep 2: Practice deep breathing exercises (e.g., inhale for 4 seconds, hold for 4 seconds, exhale for 4 seconds) to help calm your body. \nStep 3: Engage in progressive muscle relaxation to release built-up tension. \n\nSerenimind can guide you through these exercises with regular reminders to practice, helping you manage your stress responses more effectively.",
    
    "Anxiety can cause people to react in ways that feel out of control. Recognizing these reaction patterns is the first step to regaining control. \n\nStep 1: Keep a journal to track your anxiety responses, like avoidance or restlessness. \nStep 2: Identify patterns in your reactions and determine the triggers behind them. \nStep 3: Work on using techniques such as mindfulness, cognitive reframing, or relaxation exercises to break the pattern. \n\nSerenimind’s daily journaling prompts and cognitive techniques can help you stay on top of these patterns and regain control of your responses.",
    
    "Panic attacks often follow certain behavior patterns, like rapid breathing or avoidance. \n\nStep 1: Identify the early warning signs of an impending panic attack (e.g., rapid breathing, dizziness, or chest tightness). \nStep 2: Use grounding techniques such as the 5-4-3-2-1 method (identify 5 things you can see, 4 you can touch, etc.) to anchor yourself in the present moment. \nStep 3: Practice deep breathing to slow down your heart rate and manage the panic symptoms. \n\nSerenimind offers real-time support during panic moments, guiding you through these exercises and helping you regain calm.",
    
    "The way you respond to anxiety can vary from person to person. It's important to recognize your own anxiety responses to tailor strategies that work best for you. \n\nStep 1: Reflect on how you typically respond to anxiety (e.g., avoidance, irritability, or physical symptoms). \nStep 2: Identify the strategies that have worked for you in the past, such as deep breathing or cognitive restructuring. \nStep 3: Customize your coping plan with Serenimind, which allows you to set personalized strategies that align with your specific responses. \n\nThis tailored approach will help you handle anxiety more effectively over time.",
    
    "Stress can lead to habits that, while offering temporary relief, may not be effective long-term. \n\nStep 1: Identify stress-related habits that provide short-term relief but are not sustainable, such as overeating or excessive screen time. \nStep 2: Replace these habits with healthier stress-relief techniques, such as exercise, journaling, or engaging in hobbies. \nStep 3: Set achievable goals for incorporating these new habits into your daily routine. \n\nSerenimind offers guidance through habit tracking and progress monitoring to help you maintain healthy changes over the long term.",
    
    "Anxiety and panic can create specific behavior patterns that hold you back from feeling calm. Recognizing these patterns is the first step toward managing them. \n\nStep 1: Identify the specific behaviors that you notice when feeling anxious, like pacing or shallow breathing. \nStep 2: Practice breathing exercises and grounding techniques to break these patterns. \nStep 3: Work through gradual exposure to the situations that trigger your anxiety, so that you can respond in a more controlled manner. \n\nSerenimind provides step-by-step support and reminders to practice these techniques regularly, helping you build better coping patterns.",
    
    "Identifying your anxiety behaviors is the first step in breaking the cycle. Once you’ve recognized your triggers, Serenimind can help you develop healthier habits by implementing coping mechanisms like mindfulness, breathing exercises, or behavioral interventions designed to reduce the impact of anxiety on your life. \n\nStep 1: Track your anxiety behaviors and identify specific triggers. \nStep 2: Choose an alternative coping mechanism, such as breathing exercises or cognitive reframing, that works for you. \nStep 3: Practice these techniques whenever you encounter a trigger, gradually replacing the negative behaviors with healthier ones. \n\nSerenimind’s personalized approach ensures that you receive consistent support and feedback to make lasting changes.",
    
    "Sometimes, the avoidance of situations or people can be a sign of deeper anxiety. Acknowledging these avoidance behaviors is a crucial step towards regaining control. \n\nStep 1: Reflect on the situations or people you avoid due to anxiety and try to understand the underlying fears. \nStep 2: Start small by gradually confronting these fears in a controlled and safe environment. \nStep 3: Use Serenimind’s structured exposure plans and relaxation techniques to help you feel more comfortable as you face these deeper anxieties. \n\nBy taking small, manageable steps, you’ll begin to feel more in control and less overwhelmed by fear."
  ],
"Coping_Mechanisms": [
    "Managing anxiety effectively is key to maintaining emotional stability. One of the most widely recognized techniques is deep breathing. By focusing on slow, deep breaths, you can activate your body’s natural relaxation response. A method you could try is the 4-7-8 technique: breathe in for 4 seconds, hold for 7 seconds, and exhale for 8 seconds. This helps calm the mind and regulate the nervous system, especially during moments of intense anxiety.",
    
    "Mindfulness is another valuable tool in anxiety management. A simple way to practice mindfulness is by focusing on the present moment and gently guiding your attention back whenever it wanders. A quick mindfulness exercise you can use is the '5-4-3-2-1 method,' where you identify 5 things you can see, 4 things you can touch, 3 things you can hear, 2 things you can smell, and 1 thing you can taste. This helps ground you in the present and reduce overwhelming thoughts.",
    
    "To combat anxiety, progressive muscle relaxation (PMR) is an excellent strategy. PMR involves tensing and relaxing different muscle groups in the body, helping to release physical tension associated with anxiety. Start by focusing on your feet and working your way up to your head. Tense each muscle group for 5 seconds, then release. This not only relieves tension but also improves awareness of physical sensations.",
    
    "Coping with panic attacks requires a calm approach. Grounding exercises like focusing on a physical object or touching something cold, such as an ice cube, can bring your awareness back to the present moment. Pair this with controlled breathing to help regulate your body’s response and reduce the intensity of the panic attack.",
    
    "In moments of high stress, using self-compassion can be incredibly effective. Remind yourself that it's okay to feel anxious and that your feelings are valid. Engage in positive self-talk by acknowledging your strength in facing these emotions and giving yourself grace. This can help break the cycle of negative self-criticism that often worsens anxiety.",
    
    "Physical exercise is another powerful anxiety management tool. Regular exercise releases endorphins, the body’s natural mood boosters. Even something as simple as a brisk walk or stretching exercises can help improve your emotional well-being and lower stress levels. Aim for at least 30 minutes of activity a day to help manage anxiety more effectively."
  ],  
  "Emotional_Responses": [
    "When anxiety strikes, the emotional impact can often feel overwhelming. It's crucial to address these emotions head-on and not suppress them. Practice self-awareness by labeling your feelings, such as recognizing that you are feeling anxious, sad, or overwhelmed. By acknowledging these emotions, you can start to detach from them and manage their effects more effectively. Using techniques like breathing exercises or mindfulness can help regulate your emotional responses.",
    
    "The emotional toll of anxiety can manifest as fear, sadness, or irritability. It’s important to not only identify these emotions but also to understand where they’re coming from. Recognizing triggers for emotional distress can be a starting point in reducing their intensity. Cognitive Behavioral Therapy (CBT) techniques like thought reframing can be useful in challenging negative emotions and replacing them with more positive, balanced thoughts.",
    
    "If you're feeling emotionally drained by anxiety, journaling can be a powerful tool. Writing down your thoughts and emotions helps you process what you’re going through and can provide clarity on underlying issues. You could try journaling for 10-15 minutes daily, focusing on both what triggered your anxiety and what helped you feel better. This reflection can be an effective way to manage emotional responses over time.",
    
    "Stressful situations can lead to emotional exhaustion, but recognizing when you are nearing your emotional limits can help you manage this exhaustion. Practice taking breaks throughout your day to check in with your feelings. When you feel emotionally drained, engage in relaxation activities such as deep breathing or a hobby you enjoy to recharge and maintain emotional balance.",
    
    "Anxiety can also trigger feelings of frustration or anger. If you notice these emotions, it may help to practice self-compassion and remind yourself that it’s okay to experience these feelings. Taking a break from stressful situations and engaging in relaxation techniques like breathing exercises or stretching can help to manage anger and frustration caused by anxiety.",
    
    "Emotional resilience involves learning to manage and bounce back from challenging emotional responses. One effective approach is to cultivate a 'growth mindset.' This mindset encourages you to see challenges, including anxiety, as opportunities for growth and learning. Instead of seeing emotional setbacks as failures, try to view them as temporary and surmountable challenges that you can overcome with the right tools and mindset."
  ],
  "Sleep_Patterns": [
    "Sleep disruptions caused by anxiety are common, but they can be managed. Creating a calming bedtime routine is essential for signaling your body that it’s time to wind down. Try engaging in relaxing activities like reading, stretching, or taking a warm bath an hour before bed. Avoid screens during this time as the blue light can interfere with melatonin production, making it harder to fall asleep. Consistency is key, so aim for a consistent bedtime and wake-up time each day to improve your overall sleep hygiene.",
    
    "If racing thoughts are preventing you from falling asleep, one solution is to practice a relaxation technique such as progressive muscle relaxation or deep breathing. Focus on relaxing each muscle group in your body, starting from your toes and working your way up to your head. This not only calms your body but also distracts your mind from anxious thoughts. Additionally, guided sleep meditation or calming music can help ease you into a restful sleep.",
    
    "To break the cycle of anxiety affecting your sleep, you might want to try cognitive behavioral strategies. Cognitive Behavioral Therapy for Insomnia (CBT-I) is a structured approach that focuses on changing negative thought patterns that interfere with sleep. By challenging thoughts such as 'I won’t sleep well' and replacing them with positive affirmations like 'I can rest and relax,' you can train your mind to relax before bed. Along with this, avoid caffeine or heavy meals late in the day.",
    
    "If anxiety wakes you up in the middle of the night, practicing a grounding exercise can help. Focus on a specific object in the room, or use the '5-4-3-2-1' technique to redirect your attention. Slowly acknowledging one sense at a time—what you can see, touch, hear, smell, and taste—can help ease your mind and reduce feelings of anxiety that might be keeping you awake.",
    
    "Sleep difficulties often arise due to a mix of anxiety and poor sleep habits. A good starting point is to establish a bedtime routine that signals to your body it’s time to relax. Turn off all electronic devices at least 30 minutes before bed to avoid disrupting your body’s natural circadian rhythm. Additionally, creating a comfortable sleep environment by adjusting the room temperature and reducing light exposure can further promote restful sleep."
  ],
  "Mindfulness_and_Relaxation": [
    "Let's explore mindfulness and relaxation techniques together. These practices can be powerful tools for managing anxiety and finding inner calm. First, let's find a comfortable position and focus on your breath. Notice the natural rhythm of your breathing without trying to change it. As thoughts arise, acknowledge them gently and let them pass, like clouds in the sky. This simple practice can help ground you in the present moment and reduce anxiety. We can explore various techniques like body scans, guided imagery, or mindful walking to find what resonates most with you. Remember, mindfulness is a skill that develops with practice.",

    "I understand you're interested in learning about mindfulness and relaxation. These practices can help create a sense of calm and balance in your life. Let's start with a basic mindfulness exercise: focus your attention on your breath, noticing the sensation of air moving in and out of your body. When your mind wanders (which is perfectly normal), gently bring your attention back to your breath. This simple practice can help reduce anxiety and increase your awareness of the present moment. We can explore various techniques and develop a regular practice that fits your lifestyle.",

    "Thank you for showing interest in mindfulness and relaxation techniques. These practices can be valuable tools for managing anxiety and stress. Let's begin with understanding what mindfulness means: it's about being present in the current moment without judgment. We can practice this through various exercises like mindful breathing, body awareness, or gentle movement. Together, we'll explore different techniques and find what works best for you. Remember, there's no 'right' way to practice mindfulness – it's about finding what helps you feel more centered and calm.",

    "Mindfulness and relaxation can be powerful allies in managing anxiety. Let's work on developing these skills together. We can start with a simple grounding exercise: notice five things you can see, four things you can touch, three things you can hear, two things you can smell, and one thing you can taste. This helps bring your attention to the present moment and away from anxious thoughts. We'll explore various techniques like progressive muscle relaxation, guided meditation, or mindful observation to build your relaxation toolkit.",

    "I'm here to help you explore mindfulness and relaxation practices. These techniques can help reduce anxiety and create more peace in your daily life. Let's start with a basic relaxation exercise: take a deep breath in through your nose for four counts, hold for four, and exhale through your mouth for six counts. Notice how this simple practice affects your body and mind. We can build on this with various mindfulness techniques, helping you develop a regular practice that supports your emotional well-being. Remember, consistency is more important than perfection in mindfulness practice."
  ],
"Self_Awareness": [
    "I notice you're taking time to check in with yourself, which is a crucial step in emotional wellness. Let's explore your current emotional state together. Sometimes our feelings can be complex, like layers of an onion, and it's helpful to peel them back one at a time. Would you like to start by focusing on your physical sensations, your thoughts, or your emotions? Remember, there's no right or wrong way to feel - all emotions are valid and worthy of attention.",
    
    "Taking a moment for self-reflection is a powerful practice. As we explore your current state, consider not just what you're feeling, but also what might have contributed to these emotions. Think about your day so far - have there been any particular triggers or situations that stand out? Understanding these patterns can help us develop better strategies for managing your emotional well-being. Let's take this journey of self-discovery together.",
    
    "It's wonderful that you're practicing self-awareness. This is like being an emotional scientist - observing and collecting data about your inner experience. Let's start by creating a gentle space for exploration. Take a few deep breaths, and as you do, notice what's happening in your body. Are there areas of tension or comfort? What thoughts are passing through your mind? What emotions are present? Each observation helps build a clearer picture of your current state.",
    
    "Checking in with yourself is a vital skill that gets stronger with practice. As we explore your current emotional landscape, try to approach your feelings with curiosity rather than judgment. Imagine you're sitting by a stream, watching your thoughts and emotions float by like leaves on the water. What do you notice? Are there certain emotions that feel stronger than others? How long have these feelings been present? Understanding these patterns can provide valuable insights into your emotional well-being.",
    
    "Self-awareness is like building a map of your inner world. Right now, we're going to take some time to explore that terrain together. Start by noticing your breath - is it shallow or deep? Fast or slow? Then, scan your body from head to toe, noting any physical sensations. What emotions are you experiencing? Are they familiar companions or unexpected visitors? This kind of gentle exploration helps us understand ourselves better and make more informed choices about our well-being."
  ],
  "Resources_and_Education": [
    "I understand you're seeking information about anxiety, and that's a significant step toward better understanding and management. Let me share some comprehensive resources with you. First, it's important to understand that anxiety is a natural response of our body's fight-or-flight system. When we experience anxiety, our body is trying to protect us, even though it might not feel helpful in the moment. Let's explore some evidence-based information about how anxiety works in our brain and body, and then we can discuss specific strategies that might work for your situation. Would you like to start with the biological basics of anxiety, or would you prefer to focus on practical management techniques?",
    
    "Knowledge is a powerful tool in managing anxiety, and I'm here to help you build that foundation. Let's start by understanding that anxiety exists on a spectrum - from mild unease to panic attacks - and each person's experience is unique. I have access to research-backed information about different types of anxiety, their triggers, and various management approaches. We can explore everything from cognitive-behavioral techniques to mindfulness practices, medication options, and lifestyle modifications. What specific aspect of anxiety would you like to learn more about first? Remember, learning about anxiety often helps reduce its power over us.",
    
    "I'm glad you're reaching out to learn more about managing anxiety. Let me share some valuable resources with you. First, it's helpful to understand that anxiety is not a sign of weakness - it's a common human experience that affects millions of people worldwide. I can provide information about different therapeutic approaches, self-help strategies, and the latest research on anxiety management. We can also explore how lifestyle factors like sleep, nutrition, and exercise play crucial roles in anxiety levels. Would you like to start with understanding the science behind anxiety, or would you prefer to focus on practical coping strategies?",
    
    "Thank you for seeking information about anxiety. Let's build your knowledge base together. Understanding anxiety is like putting together a puzzle - each piece of information helps create a clearer picture. I can share resources about the physiological aspects of anxiety, common triggers, and evidence-based treatment options. We'll also explore how different aspects of your life - from sleep patterns to social connections - can impact anxiety levels. What specific area would you like to focus on first? Remember, learning about anxiety is often the first step toward better management.",
    
    "I appreciate your interest in learning more about anxiety management. Let me provide you with some comprehensive resources. We'll start by understanding that anxiety is not just a mental experience - it affects our whole body, from our thoughts to our physical sensations. I can share information about different types of anxiety disorders, common symptoms, and various treatment approaches. We'll also explore practical strategies you can implement in your daily life. Would you like to begin with understanding the basics of anxiety, or shall we focus on specific management techniques?"
  ],
  "Real_Time_Techniques": [
    "I hear that you need support right now, and I'm here to help you through this moment. Let's start with a comprehensive grounding technique that engages all your senses. First, find a comfortable position and take a deep breath. Now, let's practice the enhanced 5-4-3-2-1 method:\nLook around and name 5 things you can see in detail - notice their colors, shapes, and textures.\nNext, identify 4 things you can physically feel - perhaps the texture of your clothing, the temperature of the air, or the surface you're sitting on.\nListen for 3 distinct sounds in your environment, even subtle ones like the hum of electronics or your own breath.\nTry to notice 2 different scents around you, even if they're faint.\nFinally, focus on 1 taste in your mouth. Take another deep breath and notice how your body feels now compared to when we started.",

    "Let's work together to help you find calm in this moment. We'll begin with a progressive muscle relaxation technique that helps release physical tension while calming your mind.\nStart by sitting or lying comfortably. Take a deep breath in through your nose for 4 counts, hold for 4, and exhale slowly through your mouth for 6 counts.\nNow, we'll systematically tense and relax each muscle group. Start with your toes - curl them tightly for 5 seconds, then release. Notice the difference between tension and relaxation.\nMove to your feet, then ankles, calves, and continue up your body.\nWith each release, imagine stress flowing away from your body. Remember, you're safe right now, and this feeling will pass.",

    "I understand you're looking for immediate relief, and I'm here to guide you through some effective techniques. Let's start with a powerful breathing exercise called 'Square Breathing.'\nImagine tracing a square in front of you with your eyes or finger. As you trace the first side, breathe in for 4 counts. Hold your breath for 4 counts as you trace the second side.\nExhale for 4 counts along the third side, and hold for 4 counts on the final side.\nLet's repeat this cycle 4 times. Pay attention to how the rhythm of your breath becomes more regular with each cycle.\nNotice how your shoulders begin to relax and your mind becomes more focused on the present moment.",

    "I'm here to help you through this challenging moment. Let's use a comprehensive approach combining physical and mental techniques.\nFirst, place both feet firmly on the ground and feel the solid support beneath you.\nNow, place one hand on your chest and the other on your belly. We'll practice diaphragmatic breathing - breathe in slowly through your nose, letting your belly expand while your chest remains relatively still.\nHold for a moment, then exhale slowly through pursed lips, feeling your belly fall.\nAs you continue this breathing pattern, let's add a positive affirmation: 'I am safe,' on the inhale, and 'I can handle this,' on the exhale.\nRemember, anxiety is temporary, and you have the tools to move through it.",

    "Let's work together to help you find some relief right now. We'll use a combination of mindfulness and body-based techniques.\nStart by finding a comfortable position and closing your eyes if that feels safe.\nTake a moment to notice where you feel anxiety in your body - perhaps it's a tightness in your chest, butterflies in your stomach, or tension in your shoulders.\nDon't try to change these sensations yet; just observe them with curiosity.\nNow, imagine you have a warm, healing light in your hands.\nAs you breathe deeply, imagine this light flowing to those areas of tension, gradually softening and soothing them.\nWith each exhale, feel the tension dissolving a little more."
],
 "Feedback_and_Improvement": [
        "Thank you for your feedback. Based on your experience, we’ve prioritized actionable changes. For example, if the interface felt overwhelming, we recommend simplifying the navigation or highlighting the most-used features upfront. Your suggestion helps us implement clearer sections and tooltips to improve user experience. Additionally, we are adding more personalized mental health resources to better align with user needs.",
        
        "Your insights are deeply appreciated. For instance, if you've mentioned difficulty in finding resources, we’ve updated our search functionality to include categorized tags like 'Anxiety Support,' 'Breathing Exercises,' or 'Mindfulness Games.' This ensures easier access to specific content. Thank you for helping us refine this process further.",
        
        "Your feedback is crucial. If content clarity is a concern, we've implemented AI-driven content summaries to provide concise overviews of each resource. This way, users can quickly decide if a resource suits their needs. Your suggestions help us fine-tune these features to make Serenimind even more helpful.",
        
        "Thank you for highlighting areas of improvement. If accessibility was mentioned, we've added features such as adjustable font sizes, dark mode, and audio guides for all sections. These updates ensure Serenimind is inclusive and user-friendly. Your feedback drives these enhancements forward.",
        
        "We’re grateful for your feedback, especially about improving engagement. To address this, we’ve integrated daily motivational notifications and quick self-assessment tools. These features aim to keep users connected and supported throughout their mental health journey. Your feedback helps us refine and enhance these tools."
    ],   
    "Environmental_Triggers": [
        "It seems your environment is causing stress. One immediate solution is to practice grounding techniques like the '5-4-3-2-1' exercise. This involves identifying five things you see, four things you touch, three things you hear, two things you smell, and one thing you taste. This method can help you anchor yourself in the moment and reduce the impact of environmental triggers.",
        
        "To address triggers like noise or crowds, Serenimind offers a curated list of calming playlists and mindfulness podcasts accessible through the app. Additionally, noise-canceling headphones or planning breaks during crowded situations can provide relief. Let’s implement these changes together.",
        
        "Bright lights or overstimulating environments can be overwhelming. Serenimind recommends creating a 'Calm Kit'—a collection of items like sunglasses, a calming scent, or a stress ball. You can customize the kit with Serenimind’s guided suggestions tailored to your triggers.",
        
        "If your surroundings are stressful, try creating a 'Safe Space' at home. Serenimind provides step-by-step guides to set up areas with soft lighting, soothing colors, and items that bring you peace. This designated space can serve as your retreat when things feel overwhelming.",
        
        "Managing environmental stressors often starts with preparation. Serenimind’s environment planner tool allows you to input potential stressors and receive tailored coping strategies. For instance, if noise is a trigger, it will suggest noise-dampening materials or apps for sound masking."
    ],   
    "Past_Experiences": [
        "Your past experiences may influence your present, but they don’t define your future. Serenimind offers journaling templates designed to help you process those experiences step-by-step. Writing can help clarify emotions and uncover patterns, giving you control over your narrative.",
        
        "Reflecting on the past is a courageous step. Serenimind provides interactive exercises such as rewriting past experiences with a focus on lessons learned and strengths gained. This can help shift your perspective from regret to resilience.",
        
        "Understanding how the past impacts the present is vital. Serenimind’s guided meditation sessions specifically address letting go of past emotional burdens. These sessions include techniques like visualization and affirmations to help you move forward.",
        
        "To support healing from past challenges, Serenimind offers a 'Strength Map' tool. This feature highlights personal milestones and strengths developed through adversity, giving you a visual representation of how far you’ve come.",
        
        "Processing past experiences takes time. Serenimind integrates CBT-inspired exercises to help reframe negative thoughts. For example, you can list an event, identify unhelpful thoughts, and replace them with constructive alternatives—all within the app."
    ],
    "Professional_Help": [
    "Seeking professional support is a courageous step. You can book a mental health professional through Serenimind or call +2347078634362 for immediate assistance. You can also email team@serenimind.com.ng. How can I help you get started?",
    "Talking to a professional can provide tools and insights to navigate your challenges. Book a session on Serenimind, call +2347078634362, or email team@serenimind.com.ng for guidance.",
    "A therapist or counselor could offer valuable support tailored to your needs. Visit Serenimind to book, call +2347078634362, or reach out via team@serenimind.com.ng to take the next step.",
    "It's okay to seek help when you need it. You can book a session with Serenimind, call +2347078634362, or email team@serenimind.com.ng for assistance in finding the right support.",
    "Professional guidance can make a big difference in managing stress and anxiety. Book a professional through Serenimind or get in touch at +2347078634362 or team@serenimind.com.ng.",
    "Finding the right mental health professional can feel daunting, but you’re not alone. Serenimind can help you. Book now, call +2347078634362, or email team@serenimind.com.ng.",
    "Taking the step to reach out for professional support shows strength. You can book a mental health professional with Serenimind, call +2347078634362, or contact team@serenimind.com.ng for assistance.",
    "Therapy can offer a safe space to work through your feelings. Book your session on Serenimind, call +2347078634362, or email team@serenimind.com.ng to start your journey.",
    "Counselors and specialists are there to support you. Let me guide you through Serenimind to book a session, or call +2347078634362 or email team@serenimind.com.ng.",
    "Professional help can be a key part of your journey. Book with Serenimind, contact +2347078634362, or email team@serenimind.com.ng to find the resources you need."
],
"Motivational_Support": [
        "You’re doing better than you think. Every small step you take is progress, and I’m here to cheer you on.\n\n"
        "Sometimes the smallest actions, like taking a deep breath or pausing for a moment, can make a huge difference.",

        "Remember, challenges are opportunities for growth. You’ve got this, and I believe in your strength.\n\n"
        "When things feel overwhelming, focus on what you can control, even if it’s just one small thing.",

        "Even on the toughest days, your effort matters. Keep going—your resilience is inspiring.\n\n"
        "Take pride in every moment you show up for yourself, no matter how small it seems.",

        "Every day is a new chance to start fresh. Trust in your ability to navigate whatever comes your way.\n\n"
        "What’s one small thing you can do today to care for yourself?",

        "You are capable of amazing things. Let’s focus on the next step, one moment at a time.\n\n"
        "Small steps forward lead to big changes over time. Keep moving at your own pace.",

        "It’s okay to need encouragement. You’re not alone, and I’m here to support you through every moment.\n\n"
        "Lean into the support around you—it’s a strength to ask for help when you need it.",

        "Believe in your progress, no matter how small it seems. You’re stronger than you realize.\n\n"
        "What’s one accomplishment, no matter how small, that you can celebrate today?",

        "Your journey is unique, and every step forward counts. Let’s celebrate your efforts together.\n\n"
        "Progress isn’t always linear, but every moment you try is a step in the right direction.",

        "Motivation might waver, but your potential is limitless. Take it one day at a time—you’ve got this.\n\n"
        "When things feel uncertain, remember to focus on what brings you joy or peace, even for a moment.",

        "Positive energy starts with a single thought. What’s one small thing you can feel proud of today?\n\n"
        "Acknowledging the good, even in the smallest forms, can shift your perspective."
    ],
    "General_Anxiety_Assessment": [
        "It’s understandable to feel the need to assess your anxiety. While I can’t provide a diagnosis, I can guide you to recognize patterns and symptoms that might indicate anxiety.\n\n"
        "Would you like to explore an assessment tool together or discuss specific symptoms you’ve noticed?",

        "Anxiety can vary greatly from person to person. Identifying its severity often starts with recognizing how it impacts your daily life.\n\n"
        "Would you like to talk about how you’ve been feeling lately or explore self-assessment options?",

        "If you’re wondering about your anxiety levels, we can explore your recent experiences and reactions together.\n\n"
        "Remember, understanding your mental health is a courageous step. Let’s talk through it if you’re ready.",

        "Assessing your mental state can provide clarity and direction for addressing your concerns. I can help you identify common symptoms and patterns of anxiety.\n\n"
        "Would you like to begin?",

        "Understanding whether you’re experiencing anxiety can feel overwhelming, but you’re not alone.\n\n"
        "I can guide you through questions and resources that might help bring some clarity. Let’s take it one step at a time."
    ],
    "Triggers_and_Causes": [
        "Understanding the causes of anxiety is a significant step toward managing it. Often, anxiety is triggered by certain situations, environments, or recurring thoughts.\n\n"
        "One way to address this is by maintaining a journal where you document moments of anxiety. Write down the situation, how you felt, and what you were thinking at that moment. Over time, patterns may emerge, helping you pinpoint specific triggers.\n\n"
        "Once identified, you can work on minimizing exposure to these triggers or developing coping strategies, such as preparing yourself mentally before entering such situations.",

        "Anxiety triggers can be subtle, but recognizing them can empower you. Pay attention to situations or activities that consistently make you feel uneasy.\n\n"
        "For instance, if social interactions cause anxiety, you can practice by starting small, like engaging in one-on-one conversations before larger group settings. If the triggers stem from work or academic pressure, break your tasks into smaller, manageable chunks to reduce overwhelm.\n\n"
        "Seeking professional guidance to help you navigate and manage these triggers can also be highly beneficial.",

        "Pinpointing the triggers for your anxiety can be challenging but is crucial for building resilience. Start by reflecting on recent situations where anxiety spiked. Were there specific thoughts, events, or even physical sensations that preceded the feeling?\n\n"
        "Consider keeping a mental or written log of these moments. Once you recognize a trigger, work on desensitizing yourself to it through gradual exposure or reframing your thoughts about it.\n\n"
        "For example, if public speaking is a trigger, practice speaking in front of friends or a mirror before addressing a larger audience.",

        "Anxiety triggers can sometimes be linked to unresolved emotions or past experiences. Reflect on whether certain situations remind you of previous challenges or fears.\n\n"
        "Addressing these underlying causes through self-reflection or therapy can bring clarity and relief. For example, if crowded spaces make you anxious, it could be tied to a feeling of being out of control. In such cases, learning breathing techniques and grounding exercises can help you regain control over your body and mind.",

        "Recognizing anxiety triggers is the first step toward managing them effectively. Common triggers include lack of sleep, excessive caffeine, or even certain news or media content.\n\n"
        "Start by examining your daily habits and routines. Reducing caffeine, setting a regular sleep schedule, or limiting exposure to distressing news might make a big difference. It’s also important to share your feelings with a trusted friend, mentor, or professional to gain additional insights and support."
    ],

    "Physical_Symptoms": [
        "Anxiety often presents physical symptoms such as a racing heart, tense muscles, or shortness of breath. Recognizing these signs is key to addressing them effectively.\n\n"
        "If you notice your heart racing, try deep breathing exercises to calm your nervous system. Inhale deeply through your nose for four seconds, hold for four seconds, and exhale through your mouth for six seconds. Repeating this a few times can help reduce the intensity of your symptoms.",

        "Physical symptoms like headaches, stomach discomfort, or muscle tension can be overwhelming. To manage these, start by identifying when these symptoms occur. Are they linked to specific situations or thoughts?\n\n"
        "Progressive muscle relaxation (PMR) can be highly effective. This involves tensing and relaxing different muscle groups in your body, starting from your toes and moving upward. It helps release built-up tension and promotes relaxation.",

        "If you experience physical signs such as sweating, trembling, or fatigue, it may help to engage in regular physical activity. Exercise, like walking, yoga, or stretching, can reduce anxiety by releasing endorphins and lowering cortisol levels.\n\n"
        "Additionally, staying hydrated and maintaining a balanced diet can play a vital role in stabilizing your body's responses to stress.",

        "Difficulty sleeping or chest tightness can be common physical symptoms of anxiety. To address this, create a bedtime routine that promotes relaxation. Avoid screens an hour before sleep, dim the lights, and try reading or meditating to calm your mind.\n\n"
        "If chest tightness persists, grounding techniques, such as focusing on your surroundings (naming objects you see, hear, or feel), can help shift your attention away from anxious thoughts.",

        "Physical signs like dizziness or restlessness can be addressed by ensuring proper hydration and taking short breaks during stressful activities. Sometimes, simply stepping outside for fresh air or a quick walk can help re-center your mind and body.\n\n"
        "If these symptoms occur frequently, consider consulting with a healthcare provider to rule out other causes and develop a more tailored strategy."
    ],
    "Cognitive_Symptoms": [
        "Racing thoughts and persistent worry are common cognitive symptoms of anxiety. When you notice your mind spiraling, try practicing mindfulness.\n\n"
        "Mindfulness involves focusing your attention on the present moment, such as observing your breathing or the sensations in your body. Apps like Headspace or Calm can guide you through mindfulness exercises and help quiet racing thoughts.",

        "If anxiety is affecting your ability to concentrate, breaking tasks into smaller, manageable steps can help. Write down a simple to-do list and focus on completing one task at a time.\n\n"
        "Using a timer for short, focused work sessions (like the Pomodoro Technique) can help you stay on track without feeling overwhelmed.",

        "Persistent overthinking or fear of worst-case scenarios can be mentally exhausting. To combat this, try cognitive restructuring. Write down the anxious thought, then challenge it with evidence or a more balanced perspective.\n\n"
        "For example, if you think, 'I will fail this task,' counter it with 'I’ve prepared well, and I can ask for help if needed.' This practice can help reframe negative thoughts into more constructive ones.",

        "When your mind feels foggy or stuck in a loop of negative thinking, engaging in creative activities like journaling, drawing, or even listening to music can help redirect your focus.\n\n"
        "Additionally, practicing gratitude by listing three things you’re thankful for each day can shift your mindset to a more positive outlook.",

        "Thoughts spiraling out of control can feel overwhelming, but structured breathing or visualization exercises can help.\n\n"
        "Try imagining a peaceful scene, like a beach or forest, and focus on the details: the sounds, colors, and smells. This mental imagery can help break the cycle of anxious thoughts and provide a sense of calm."
    ],
    "Social_Impact": [
        "Social connections are vital to your mental well-being, as they offer emotional support, a sense of belonging, and practical assistance in times of need. If you’re feeling isolated, start small.\n\n"
        "1. Reach Out to Trusted Individuals: Make a list of people you trust, whether they’re friends, family members, or colleagues. Begin by sending a simple message, like 'Hi, I was thinking about you and wanted to check in.' Small steps can rebuild connections over time.\n\n"
        "2. Join a Community or Support Group: Look for local or online support groups that match your interests or challenges. For example, joining mental health forums, hobby-based groups, or community volunteer programs can help you connect with like-minded individuals.\n\n"
        "3. Practice Open Communication: Share your feelings with someone you trust. You don’t have to share everything at once; even small admissions like, 'I’ve been feeling a bit down lately,' can foster understanding and emotional support.\n\n"
        "4. Limit Social Media Usage: Social media can sometimes worsen feelings of isolation. Consider reducing your time online and focusing on in-person or one-on-one connections.\n\n"
        "5. Professional Guidance: If social anxiety or past trauma is making connections difficult, a therapist can provide practical tools like cognitive behavioral techniques to address these challenges.\n\n"
        "Remember, rebuilding social relationships takes time, but with consistent effort, you can create meaningful and supportive connections."
    ],
    "Severity_and_Frequency": [
        "Understanding the severity and frequency of your symptoms is crucial for creating an effective plan to manage them. Here’s a detailed guide to help:\n\n"
        "1. Keep a Symptom Journal:\n"
        "   - Track when symptoms occur, their intensity (on a scale of 1 to 10), and the circumstances leading up to them. For example, note if stress, diet, sleep patterns, or specific events trigger your symptoms. Journaling provides insights into patterns and triggers.\n\n"
        "2. Adopt Lifestyle Changes:\n"
        "   - Sleep: Create a consistent sleep routine, aiming for 7-9 hours per night. Avoid screens 1 hour before bed and try relaxing activities like reading or meditation.\n"
        "   - Diet: Incorporate mood-boosting foods rich in omega-3s (like salmon), magnesium (spinach, nuts), and vitamin D (sunlight or supplements). Reduce caffeine and sugar intake to stabilize energy levels.\n"
        "   - Exercise: Engage in at least 30 minutes of moderate exercise (like walking or yoga) 5 times a week. Exercise boosts endorphins and can reduce the frequency of symptoms over time.\n\n"
        "3. Implement Stress-Relief Practices:\n"
        "   - Mindfulness Meditation: Spend 10-15 minutes daily focusing on your breath or practicing body scans. Apps like Headspace or Calm can guide you through the process.\n"
        "   - Deep Breathing Exercises: Practice diaphragmatic breathing by inhaling deeply for 4 counts, holding for 4 counts, and exhaling for 6 counts. This calms the nervous system and reduces stress.\n\n"
        "4. Identify and Manage Triggers:\n"
        "   - Review your journal for common triggers. For example, if crowded spaces trigger symptoms, try gradual exposure therapy where you slowly build tolerance to those environments.\n"
        "   - Develop an action plan for high-stress situations. For instance, if deadlines increase symptoms, break tasks into smaller steps and allocate more time for completion.\n\n"
        "5. Seek Professional Help:\n"
        "   - For severe symptoms that interfere with daily life, consult a mental health professional. They may recommend therapies such as Cognitive Behavioral Therapy (CBT), medications, or a combination tailored to your needs.\n"
        "   - Therapists can also teach coping strategies for symptom management and provide a safe space for exploring underlying issues.\n\n"
        "6. Engage in Peer Support:\n"
        "   - Sometimes, talking to others who have experienced similar challenges can be incredibly validating and helpful. Join support groups where members share coping techniques and offer encouragement.\n\n"
        "Severity and frequency can feel overwhelming, but consistent application of these techniques, along with professional guidance, can help reduce their impact and improve overall well-being."
    ],
"Depression_Symptoms": [
    "Depression can often feel overwhelming, but recognizing the symptoms is the first step towards healing. Common signs include persistent feelings of sadness, loss of interest in activities, and difficulty concentrating. You may also experience changes in appetite, sleep disturbances, or a general sense of fatigue. It’s important to pay attention to how you’re feeling and to seek help early. Start by reaching out to someone you trust and sharing your emotions. Additionally, creating a routine, even if it's a small one, can help to restore a sense of control. If you’re struggling, booking a session with a therapist through Serenimind can provide personalized support to navigate through these feelings.",
    
    "It's okay to feel like you’re carrying a heavy weight when dealing with depression. Some signs to look for are consistent low moods, hopelessness, or withdrawal from social activities. These feelings are valid, but they don’t define you. Focus on taking small steps – even something as simple as getting out of bed and stretching can begin to make a difference. If you're noticing these symptoms, it’s important to seek professional help. A therapist at Serenimind can work with you to develop coping strategies and help you manage the emotional weight you may be carrying."
],
"Depression_Coping_Strategies": [
    "Coping with depression requires a multi-faceted approach that includes both physical and emotional strategies. Start by creating a daily routine, as structure can provide a sense of stability. Aim to get up at the same time each day, take small walks, and make time for hobbies, even if they don’t seem appealing at first. It’s essential to challenge negative thinking patterns by focusing on your strengths and reminding yourself of past accomplishments. Journaling your feelings and engaging in creative outlets can also help you process emotions. If you find it difficult to navigate these strategies alone, Serenimind can connect you with a therapist who can provide guidance and support tailored to your needs.",
    
    "When dealing with depression, it’s vital to remember that healing takes time. One strategy is practicing mindfulness to become more present in the moment, reducing feelings of overwhelm. Focus on breathing exercises that help calm your nervous system. In addition, reaching out to a trusted friend or family member can help break the isolation. Ensure you're getting adequate rest, as sleep disturbances can worsen depression. Consider engaging in light physical activity like yoga or walking to improve mood. If you need further support, booking a session with one of Serenimind's licensed therapists can provide you with expert guidance."
],
"Seeking_Professional_Help": [
    "Seeking professional help for depression is one of the most effective ways to start your healing journey. A therapist can help you explore the underlying causes of your depression and work with you to develop healthy coping mechanisms. Cognitive Behavioral Therapy (CBT) is a popular treatment that helps you identify negative thought patterns and replace them with more balanced perspectives. Sometimes, therapy involves looking at past experiences to understand current behaviors. If you are feeling overwhelmed, booking a therapy session on Serenimind can provide you with access to licensed professionals who specialize in treating depression.",
    
    "It’s a sign of strength to acknowledge when you need professional support. A therapist can help you explore the root causes of your depression and work with you to identify solutions. Therapy could involve various techniques, such as talk therapy, cognitive restructuring, or behavioral therapy, all tailored to your specific needs. It’s important to remember that healing is a journey, and therapy can give you the tools to navigate that journey with confidence. If you're ready, Serenimind offers easy access to therapists who can support you every step of the way."
],
"Depression_Support_Network": [
    "Building a support network is one of the most powerful tools you can use when managing depression. Isolation often exacerbates feelings of sadness, so it’s important to stay connected with others, whether through family, friends, or support groups. While it can be hard to open up, sharing your feelings with trusted individuals can create a sense of relief and connection. There are also online communities, both public and private, where people share their experiences with depression. These groups can help you feel less alone. If you're unsure where to start, Serenimind can guide you to support groups or professional therapists who specialize in creating healthy support systems.",
    
    "It’s essential to have a support system when navigating depression. Isolation can amplify feelings of loneliness and sadness, so connecting with others who understand can make a huge difference. Seek out a trusted family member, friend, or support group where you can express yourself freely. Talking to others who are going through similar experiences can also help you realize that you're not alone. If you feel comfortable, you can reach out to a Serenimind therapist who can help you identify and strengthen your support network."
],
"Depression_Affirmations": [
    "Affirmations are a powerful tool to help counteract the negative self-talk that often accompanies depression. Begin by creating a list of positive statements that resonate with you. Some examples include, 'I am worthy of love and happiness,' or 'I have the strength to face this.' These affirmations can be repeated daily, especially during difficult moments, to shift your mindset and reframe your thoughts. Over time, you’ll find that these positive statements begin to overwrite negative thought patterns. Consistency is key, and if you need guidance on how to use affirmations more effectively, a Serenimind therapist can help integrate them into your daily routine.",
    
    "Using affirmations can create a strong foundation for building self-compassion and confidence. Start each day with an affirmation that reflects your strength, such as 'I am capable of overcoming challenges.' Even on days when it feels impossible, remind yourself that healing is a journey, and it’s okay to take small steps. Keep your affirmations visible, on sticky notes or your phone, so they serve as a constant reminder of your worth. If you’re unsure how to incorporate affirmations into your routine, a therapist on Serenimind can guide you."
],
"Depression_Exercise_Tips": [
    "Exercise is a natural way to combat depression as it helps release endorphins, the body’s mood-boosting chemicals. Start small with activities like walking or gentle stretching. Aim for at least 30 minutes of light exercise per day, but don’t feel pressured to do more than you’re comfortable with. Even small actions, such as taking the stairs or stretching while watching TV, can help lift your mood. In addition to physical activity, try incorporating relaxation exercises such as yoga or tai chi, which combine movement with mindfulness. If you find it difficult to get started, booking a session with a therapist through Serenimind can help you build a plan that works for you.",
    
    "Exercise is a proven method to alleviate symptoms of depression. Even though it may feel challenging, starting with light movement, such as a short walk or some basic stretches, can make a difference. Physical activity not only helps reduce stress but also improves sleep and boosts overall well-being. Set realistic goals, and remember that every small step counts. Additionally, combining exercise with deep breathing techniques can enhance the benefits. If you need help developing an exercise plan tailored to your needs, consider booking a therapy session through Serenimind."
],
"Depression_Sleep_Tips": [
    "Sleep issues are common with depression, but establishing a consistent sleep routine can improve both your sleep quality and mood. Start by creating a calming bedtime ritual, such as reading a book or listening to soothing music, to help signal your brain that it’s time to wind down. Avoid caffeine or alcohol close to bedtime, as these can interfere with your sleep. Keep your bedroom environment comfortable, dark, and quiet. A consistent sleep schedule is also crucial – aim to wake up and go to bed at the same time every day. If sleep disturbances persist, reach out to a therapist through Serenimind to address underlying causes of poor sleep.",
    
    "Good sleep hygiene is a key factor in managing depression. Start by setting up a calming pre-sleep routine, such as a warm bath or relaxation exercises, to ease your body into rest. Avoid screen time at least 30 minutes before bed, as the blue light emitted can disrupt your sleep. Also, try to keep your sleep environment quiet, cool, and dark. If you're struggling to sleep despite following these tips, it may be helpful to talk to a therapist who can assist you in addressing any underlying issues. Serenimind can connect you to a professional therapist to help improve your sleep."
],
"Depression_Mindfulness_Techniques": [
    "Mindfulness techniques can help you stay grounded when you're feeling overwhelmed by depression. Start by focusing on your breath: take a deep breath in for a count of four, hold for four, and exhale for four. Practice this a few times to calm your nervous system. You can also use a technique called 'body scan' where you mentally check in with each part of your body, noticing any tension and consciously relaxing it. Regular mindfulness practices can create a sense of calm and help you stay connected to the present. If you find it difficult to start practicing mindfulness on your own, a Serenimind therapist can guide you through it.",
    
    "Mindfulness is an effective way to manage the emotional turbulence that comes with depression. One simple practice is to sit comfortably, close your eyes, and pay attention to your breath. When your mind begins to wander, gently bring your focus back to your breath. You can also practice mindfulness while doing everyday activities, such as eating or walking, by fully engaging in the experience without judgment. Over time, mindfulness can help reduce anxiety and depressive thoughts. If you're unsure how to start, Serenimind can connect you with a therapist who specializes in mindfulness techniques."
],
 "Feeling_Overwhelmed_Stressed": [
    "When you feel overwhelmed, it’s crucial to break down your tasks into manageable steps. Start by tackling the most urgent one, and give yourself a break afterward. Also, try deep breathing exercises to lower your stress levels.",
    "Take a moment to breathe. When stress becomes overwhelming, focusing on one task at a time can help. Also, consider scheduling some relaxation time each day to recharge and prevent burnout.",
    "Stress is tough, but small actions can help. Start by prioritizing your most important tasks, and don’t hesitate to ask for help from someone if needed. You can also incorporate daily relaxation exercises like yoga or meditation to lower anxiety.",
    "Overwhelming feelings often come from taking on too much at once. Break down your goals into small tasks, and focus on completing one thing at a time. Use mindfulness techniques, like taking deep breaths or going for a walk, to clear your mind.",
    "It’s okay to feel stressed. To manage it, create a simple plan for your tasks. A good strategy is the 'Pomodoro technique'—work for 25 minutes, then take a 5-minute break. Don’t forget to check in with yourself regularly and practice relaxation exercises."
  ],
"Journaling_and_Self_Reflection": [
    "Journaling is a fantastic tool for self-reflection. Start by writing about how you feel in the moment, or reflect on what went well today. Use prompts like 'What am I grateful for today?' or 'What did I learn about myself?' to guide your entries.",
    "To begin journaling, write freely without worrying about structure. You can try answering questions like 'How am I feeling right now?' or 'What made me smile today?' It’s about understanding your thoughts and emotions.",
    "Journaling helps bring clarity. Write about your experiences and emotions to better understand yourself. Consider using prompts like 'What challenges did I face today?' or 'How did I cope with them?' to explore your mental state.",
    "A great journaling approach is to write without restrictions. Try describing your current mood, then reflect on the reasons behind it. This practice helps you identify patterns in your emotions and thoughts over time.",
    "Incorporate self-reflection into your journaling by asking yourself questions like 'What am I proud of today?' or 'What could I do differently next time?' This encourages growth and a better understanding of your feelings."
  ],
"Depression_Talking": [
    "Depression can feel isolating, but it’s treatable. Reaching out to a mental health professional is the first step, and focusing on daily routines can help, too. Try to get outside, engage in physical activity, and practice self-care.",
    "If you think you're struggling with depression, it's important to talk to a professional. Additionally, try to engage in activities that you enjoy, even if it feels hard. Small steps like these can help improve your mood over time.",
    "Dealing with depression can feel exhausting, but there is help available. Start by talking to a therapist, and try incorporating daily physical activity to boost your mood. Self-care practices like sleep and nutrition are equally important.",
    "Managing depression often requires a combination of therapy, lifestyle changes, and self-care. Consider building a routine with small steps like getting outside, focusing on positive thoughts, and practicing mindfulness.",
    "If you’re feeling hopeless, know that it’s important to seek help. Therapy and medication can significantly improve mental health. Additionally, practicing small positive habits like gratitude journaling and regular exercise can support your journey."
  ],
"PTSD_Questions": [
    "PTSD can develop after experiencing traumatic events, and it’s important to seek professional help for treatment. Therapies like CBT (Cognitive Behavioral Therapy) and EMDR (Eye Movement Desensitization and Reprocessing) are commonly used to manage symptoms.",
    "If you suspect you have PTSD, talking to a mental health professional is crucial. In addition, grounding techniques, mindfulness, and staying connected with supportive people can help reduce the intensity of triggers.",
    "PTSD is a natural response to trauma, and it’s treatable. Cognitive-behavioral therapy (CBT) and trauma-focused therapies can help you work through your symptoms. Also, engaging in physical activities and relaxation techniques can aid your recovery.",
    "To manage PTSD, therapy is often the first line of treatment. Techniques like grounding exercises, mindfulness, and building a supportive network can significantly help with daily triggers and emotional regulation.",
    "Seeking help from a professional is essential if you suspect PTSD. In the meantime, practicing grounding techniques, maintaining a regular sleep schedule, and managing stress through exercises like deep breathing can help."
  ],
"Loneliness_Talking": [
    "Loneliness can feel overwhelming, but it’s important to reach out to others when you can. Joining online communities, picking up a hobby, or volunteering can help create meaningful connections and reduce isolation.",
    "When you’re feeling lonely, it’s vital to remind yourself that it’s okay to reach out. Try connecting with others through online communities or support groups. Engaging in activities that bring you joy can also help combat those feelings.",
    "Overcoming loneliness starts with taking small steps toward connection. You could join a group or online community, reach out to friends or family, or start a hobby that excites you. It’s about building relationships that are meaningful to you.",
    "Loneliness often feels like an emotional gap, but it can be filled by connecting with others or discovering new interests. Consider attending local events or using social media to build connections. Self-compassion also helps by treating yourself with kindness.",
    "Loneliness can be eased by making small efforts to connect with others, whether it’s through conversations, joining an interest group, or talking to a counselor. Focusing on personal hobbies or new experiences can also help you feel more connected."
  ],
"Seeking_Support": [
    "Mental health support is key to managing tough times. Consider finding a therapist or counselor in your area or using online therapy platforms. You can also practice self-care techniques like journaling or meditation in the meantime.",
    "Seeking professional help is the first step. You can find a therapist online or through local health centers. Additionally, try supporting your mental health with activities like exercise, mindfulness, or talking to a trusted friend or family member.",
    "Reaching out to a professional therapist can help you navigate your emotions. You might also find comfort in connecting with support groups or communities. In the meantime, self-care strategies like practicing gratitude or mindfulness can support your mental well-being.",
    "When seeking support, consider talking to a licensed therapist, counselor, or a mental health hotline. Also, taking time for self-care, like deep breathing or exercise, can be beneficial in managing stress and maintaining balance.",
    "Finding the right mental health support starts with reaching out to professionals, whether in-person or online. While waiting for therapy, focusing on self-care practices like mindfulness or journaling can help manage emotions."
  ],
"Writing_Down_Thoughts": [
    "Writing down your thoughts is a powerful way to manage your emotions and reflect on your experiences. Journaling can help you organize your thoughts and relieve stress. It’s also a great way to track your mental health over time.",
    "Journaling is a wonderful practice for self-reflection. Writing down your thoughts daily helps you process emotions, reduce stress, and improve your mental clarity. It can also act as a safe space to express yourself without judgment.",
    "If you're writing down your thoughts, you're already taking a big step in managing your mental health. Journaling helps you understand your emotions, track patterns, and find ways to improve your well-being.",
    "Writing down your thoughts is a great method for self-expression. It can be a way to release emotions and track your mental health. If you're not sure where to start, you can use prompts like 'What am I grateful for today?' or 'What challenged me this week?'",
    "Journaling allows you to process your feelings and gain perspective on your life. It's an effective way to decrease stress and increase emotional awareness. Keep it simple: write what’s on your mind and reflect on how you’re feeling."
  ],
"Signs_Of_Depression": [
    "Depression can manifest in several ways, including persistent sadness, loss of interest in activities you once enjoyed, changes in appetite or sleep patterns, fatigue, and difficulty concentrating. It’s important to talk to a mental health professional if you notice these signs.",
    "Some common signs of depression include feeling hopeless, withdrawing from social activities, having trouble sleeping or sleeping too much, changes in eating habits, and feeling overwhelmed or worthless. Seeking support is a crucial first step.",
    "Depression can show up as mood changes, loss of energy, irritability, and lack of motivation. If you're experiencing these symptoms regularly, it's important to reach out to a professional who can guide you through your emotions.",
    "Signs of depression can include emotional numbness, withdrawal from social interactions, fatigue, and trouble with everyday tasks. If you're experiencing these symptoms, consider reaching out to a mental health professional for a proper assessment.",
    "Common symptoms of depression include persistent sadness, irritability, difficulty concentrating, sleep disturbances, and a lack of interest in activities. If you're feeling overwhelmed by these feelings, it’s important to seek help and support."
  ],
"No_One_To_Talk_To": [
    "It can be really tough when you feel like there's no one to talk to. While it may seem isolating, consider reaching out to a support group or professional counselor. Many people can offer help even if you feel alone right now.",
    "Feeling like you have no one to talk to can be overwhelming, but it's important to remember that help is available. You can reach out to online communities, hotlines, or even a mental health professional for support.",
    "When you're feeling like there's no one to talk to, it might help to express your feelings through journaling or consider joining a community group where people share similar experiences. Therapy or counseling could also offer a safe space to talk openly.",
    "If you're feeling alone and need someone to talk to, there are mental health professionals and online platforms where you can connect. Talking to a therapist or counselor can provide the support and guidance you need during tough times.",
    "Though it feels lonely, reaching out to a mental health professional, even online, can make a difference. There are also mental health apps and communities that provide non-judgmental spaces to talk and get support."
  ],
"Can_You_Help_Me": [
    "I'm here to help! If you're struggling with something specific, let me know, and we can work through it together. I can suggest activities, resources, or guide you in seeking professional support.",
    "Yes, I can definitely help. Whether it's managing stress, understanding your emotions, or finding support, I'm here to provide guidance. Let me know what you need, and we can work on it step-by-step.",
    "I’m here to offer support. If you're dealing with mental health challenges, I can suggest resources or techniques that might help, whether it's journaling, mindfulness exercises, or reaching out to professionals for further assistance.",
    "I can help by guiding you through various self-care practices or recommending helpful resources. Whether you’re feeling overwhelmed or need a direction to take, I’m here to offer solutions and make sure you feel supported.",
    "You’re not alone. I can help by offering self-help strategies, like breathing exercises or mindfulness techniques. I can also recommend talking to a mental health professional if you're looking for personalized support."
  ],
"Distancing_From_Toxic_Friends": [
    "It’s healthy to distance yourself from people who drain your energy or make you feel worse about yourself. Focus on surrounding yourself with positive influences and people who uplift you. It might be hard at first, but you’re doing what's best for your well-being.",
    "Cutting ties with toxic friends can be an important step in prioritizing your mental health. Focus on self-care, and remember that it’s okay to set boundaries. Surround yourself with supportive people who value and respect you.",
    "Distancing yourself from toxic people is an act of self-care. It can be difficult, but setting clear boundaries and prioritizing your mental health will lead to growth and healthier relationships in the future.",
    "It’s important to let go of relationships that aren’t serving you positively. Focus on your growth and healing by surrounding yourself with people who respect your boundaries and support your mental health.",
    "Letting go of toxic friendships is a way to create space for your own personal growth. It’s not about cutting people off permanently, but about creating boundaries that allow you to protect your peace and mental health."
  ],
"Anxiety_and_Depression": [
    "Anxiety and depression are mental health conditions that can often occur together. Anxiety involves feelings of worry or fear, while depression can lead to feelings of sadness and hopelessness. Both conditions are treatable, and professional help can guide you toward effective treatment options.",
    "Anxiety is characterized by persistent worry, fear, or nervousness, while depression involves feelings of sadness, hopelessness, and lack of energy. Both are common, and with the right support and treatment, they can be managed and improved over time.",
    "Anxiety can make you feel restless or uneasy, while depression might lead to a lack of motivation and a sense of hopelessness. Understanding these conditions and seeking therapy can help you learn coping strategies and begin healing.",
    "Anxiety and depression are both mental health conditions that affect your emotional and physical state. Anxiety often manifests as excessive worry, while depression can cause a lack of interest or energy. Treatment can help you manage both effectively.",
    "Anxiety leads to constant worry, while depression causes deep sadness and often a lack of motivation. Both conditions can significantly impact your daily life, but through therapy, medication, and self-care practices, they can be managed."
  ],
"Time_Management_and_Procrastination": [
    "If you’re struggling with time management, start by breaking your tasks into smaller steps. Use a planner or time-blocking method to stay organized. Setting realistic goals for the day and eliminating distractions will also help you stay on track.",
    "Procrastination often comes from feeling overwhelmed or unsure where to start. Try setting small, achievable goals and rewarding yourself when you complete them. A productivity technique like Pomodoro (work for 25 minutes, take a 5-minute break) can also boost focus.",
    "Managing your time starts with recognizing where you’re spending it. Create a to-do list with deadlines and prioritize tasks based on importance. Break larger tasks into smaller steps, and try not to focus on perfection—just progress.",
    "If you keep procrastinating, try setting small and realistic goals for the day. Use a timer or set clear deadlines for each task. Don’t forget to eliminate distractions like social media and focus on one task at a time.",
    "To get better at managing your day, try organizing tasks into categories: urgent, important, and less important. Use techniques like time blocking or the 'two-minute rule' (if a task takes less than two minutes, do it now) to stay focused and productive."
  ],
"Overwhelming_Depression_Feeling": [
  "Feeling overwhelmed does not necessarily mean you're depressed, but it can be a sign of stress, anxiety, or burnout. It's important to take a step back and assess how long you've been feeling this way. If you're experiencing prolonged sadness, loss of interest in activities, or changes in sleep and appetite, these could be signs of depression. Consider talking to a professional for an accurate assessment and guidance.",
  
  "Being overwhelmed is often linked to high stress, poor time management, or unmet expectations. It’s not always a sign of depression. However, if you notice that these feelings persist, and you're struggling to cope with everyday tasks or are feeling hopeless or fatigued, it could indicate depression. It’s a good idea to consult with a therapist who can help you differentiate between the two and provide support."

  "While feeling overwhelmed is a common experience, it’s not the same as depression. Depression tends to be a more prolonged state, where individuals feel a deep sense of sadness, hopelessness, and a loss of interest in things they once enjoyed. If your overwhelming feelings are paired with these signs or have lasted for weeks, it might be worth talking to a professional to explore if it’s depression or just stress."

  "Overwhelmed feelings can come from external stressors like school, work, or family obligations, and they don’t always mean you’re depressed. However, if this overwhelming feeling persists and starts affecting your day-to-day life, such as difficulty getting out of bed, avoiding social activities, or struggling with your responsibilities, it’s important to assess whether it might be a deeper issue like depression."

  "Overwhelm can be a symptom of both anxiety and depression, but it’s not always the same thing. Depression typically involves a pervasive low mood, loss of energy, and a lack of interest in life. If you're unsure whether your feelings of overwhelm are more than just stress, consider tracking your symptoms and speaking to a mental health professional who can help you determine whether you need further support."
],
"Not_Depressed": [
  "It sounds like you’re dealing with stress and feeling overwhelmed by your responsibilities, but that doesn't automatically mean you're depressed. Stress and overwhelm can cause anxiety, exhaustion, and frustration, which are common reactions to having a lot on your plate. To manage this, focus on stress-reduction techniques like mindfulness, setting small achievable goals, and getting proper rest. However, if these feelings linger or start to affect your daily activities, it may be helpful to reach out to a professional for further support.",

  "It’s possible that you're not experiencing depression, but rather a normal response to the demands of life. Overwhelm can stem from many things like workload, personal expectations, or feeling stretched too thin. Consider implementing time management strategies, taking breaks, and prioritizing self-care. If you’re still feeling burnt out or disconnected, it might be worth seeking guidance from a mental health professional to ensure there are no underlying issues."

  "Not being depressed doesn’t mean that overwhelm isn’t affecting your mental health. Overwhelm can cause feelings of anxiety and frustration. It may help to reassess your goals and break them down into manageable tasks. Practice stress management techniques like deep breathing or meditation, and remember that it’s okay to ask for help when you need it. If the feelings of overwhelm persist and start affecting your daily functioning, talking to a counselor might be beneficial."

  "It’s okay to feel overwhelmed without being depressed, but it's important to check in with yourself. Overwhelm can be caused by external pressures, like tight deadlines, family obligations, or other responsibilities. It's essential to take time for self-care, practice healthy time management, and set boundaries. However, if you notice persistent fatigue, irritability, or difficulty enjoying things you usually do, it might be a good idea to speak with a mental health professional to rule out any underlying concerns."

  "Feeling overwhelmed doesn’t automatically mean you’re depressed, but it’s crucial to address the root cause. Try breaking down your tasks into smaller, more manageable steps, and focus on prioritizing self-care, including regular breaks and sleep. However, if the feelings of being overwhelmed are causing you significant distress or affecting your daily life, it could be helpful to talk with a mental health professional to ensure that you're managing it effectively and to rule out depression or anxiety."
],
"Academic_Balance_and_Time_Management": [
    "Managing time effectively during academic life can feel like juggling, but it’s all about finding a structure that works for you. Start by prioritizing tasks. Break your assignments into smaller, more manageable chunks and create a to-do list for each day. You can track your progress through our wellness goal setter and journal your daily experiences in the Serenimind Journals. These tools will help you stay organized and motivated. If you’re feeling overwhelmed, our blogs have great time-management strategies, and if things get too much, booking a session with a professional through Serenimind could provide you with personalized support.",
    
    "A great way to balance academics with mental well-being is to stick to a routine, but one that’s flexible. Set clear boundaries for study hours and relaxation periods. It’s easy to get consumed by academic pressure, but remember that your mental health is just as important. Use our wellness goal setter to organize your daily routine, and our Journals for reflecting on your feelings. If balancing everything feels like too much, a therapist can help you with coping mechanisms tailored to your needs, and you can book one directly on our platform.",
    
    "Being a student doesn’t mean you have to sacrifice your mental health for grades. One of the best ways to find balance is to set clear expectations for yourself. Don’t hesitate to say no to activities that add unnecessary stress. And make sure your schedule isn’t packed to the brim. You need time to recharge. Take breaks when needed, whether it’s a quick meditation session, journaling, or reading one of the books on Serenimind that help reduce stress. If this strategy feels challenging, a therapist can provide emotional support and guide you to effective techniques that will help.",
    
    "The first step in academic balance is realizing that it’s okay to take a step back when things get overwhelming. Instead of focusing on everything at once, tackle one thing at a time. Utilize task batching—group similar tasks together so you can focus better. If you're feeling too stressed or lost, try journaling your thoughts, setting daily wellness goals, and reflecting through our tools. If you need more personalized support, booking a therapist through Serenimind can give you the help you need to prioritize both your academic and mental health needs."
],
"Mental_Health_and_Wellbeing": [
    "Prioritizing mental health during stressful times is crucial. First, acknowledge your feelings and give yourself permission to experience them. When emotions run high, grounding techniques like deep breathing or mindfulness can help bring you back to the present moment. You can also practice positive self-talk and reflect on what you’ve already achieved using Serenimind Journals. If the stress continues to build up, seeking professional support through our platform will guide you in developing strategies like Cognitive Behavioral Therapy (CBT) to find healthier ways to cope.",
    
    "If you're feeling mentally drained, it’s important to shift your focus towards self-care. Start by getting enough sleep, eating balanced meals, and staying hydrated. Exercise, even light walking, has been shown to improve mood by releasing endorphins. Our wellness goal setter can help you track your self-care habits, and our Journals can provide a safe space for emotional reflection. If you’re still feeling overwhelmed or stuck, don’t hesitate to book a therapist through Serenimind who can help you work through these emotions and offer support.",
    
    "Mental well-being is all about balance. Begin with small steps like setting boundaries to avoid overcommitting yourself. It’s essential to make time for things that bring you joy—whether that’s hobbies, spending time with loved ones, or simply taking a walk in nature. If you're unsure how to structure your day, use the wellness goal setter to plan self-care activities, or look through our blogs for tips on boosting your mood. If you feel like things are still too overwhelming, a therapist can provide guidance and teach you coping techniques specific to your situation.",
    
    "Sometimes it feels like mental health and academic life are in constant competition. But your well-being doesn’t need to take a backseat. One key strategy is practicing mindfulness. This could involve focusing on your breath for a few minutes each day or setting aside time for meditation. Incorporate this into your day using our wellness goal setter to remind you to take breaks. If you’re feeling stuck or need more direction, journaling can help you express what you’re feeling, and a therapist is available through Serenimind to guide you through any tough emotions."
],
"Social_Life_and_Academic_Balance": [
    "Striking a balance between academics and social life doesn’t mean giving up one for the other. It’s about setting boundaries that protect your time. A good first step is to organize your week—allocate specific times for study and other times for socializing. Prioritize quality over quantity in your social engagements. Track your emotional state and social commitments through Serenimind Journals to gain clarity. If balancing both areas feels like too much, booking a therapist via Serenimind can provide the tools to help you manage your time and energy better.",
    
    "A healthy social life is part of your overall well-being. To make it work alongside academic demands, try organizing your time so that you’re not overwhelmed. For example, plan study sessions early in the day, and use your evenings or weekends to catch up with friends or engage in group activities. Saying ‘no’ is an important skill too—don’t overextend yourself. If this feels hard to navigate, use our wellness goal setter to plan both academic and social activities and our Journals to reflect on how your social life is impacting your mental health. A therapist can provide extra support to help you create healthier boundaries.",
    
    "Balancing academics and social life is a skill that takes time to develop. Start by setting clear expectations for both areas—be realistic about how much time you can dedicate to your studies and your social activities. Use a planner or our wellness goal setter to keep track of commitments, and make sure you schedule ‘me-time’ to avoid burnout. If you’re feeling disconnected from your social life or struggling to juggle responsibilities, a therapist can offer strategies to help you find balance and prioritize your mental well-being.",
    
    "If you're finding it hard to balance social engagements with academic demands, the first step is to assess your priorities. What’s most important in the short term? Schedule your study time first, then plan social activities around that. Also, try to involve friends in activities that help you relax, like study sessions, walks, or attending events together. If things feel off-balance, journaling your thoughts, setting wellness goals, and booking a therapist through Serenimind could help you create a more manageable routine."
],
"Spiritual_and_Academic_Balance": [
    "Spirituality can be a grounding force during times of academic stress. The key is to integrate spiritual practices into your routine without overwhelming yourself. Set aside 10 minutes each morning for prayer, meditation, or reflection before diving into your academic work. Regular moments of spiritual connection can offer peace and clarity, even amidst deadlines. If balancing both feels tough, try journaling about your spiritual experiences, use the wellness goal setter to track your spiritual practices, and book a therapist through Serenimind for guidance.",
    
    "Maintaining spiritual health while managing academic demands requires intentionality. Schedule regular moments throughout your day for prayer or mindfulness, even if it’s just five minutes of reflection before you start studying. It’s important not to neglect this part of your life. If balancing both feels overwhelming, use Serenimind's wellness goal setter to organize both your academic and spiritual commitments, and consider journaling about your thoughts. A therapist can provide tailored advice to help you integrate both effectively.",
    
    "Your spiritual life is important, and it’s essential to ensure that it’s not compromised in the hustle of academic life. Try to incorporate small moments of spirituality throughout your day, whether through reading spiritual texts, prayer, or meditation. You can even combine your spiritual practices with activities like walking or exercise. If you're unsure how to make time for both, use Serenimind’s wellness goal setter to plan your day and track your spiritual growth. A therapist can also offer advice on maintaining spiritual well-being while meeting your academic goals.",
    
    "Creating space for spirituality in your academic life is not about doing everything at once but about making time for moments that nourish your soul. Set aside time for meditation or spiritual reflection, especially during high-stress periods. By doing this, you can create a balance that nurtures both your mental health and academic focus. If you’re feeling disconnected, journaling your thoughts or booking a therapist session through Serenimind can help you align both your spiritual and academic needs."
],
"Coping_Strategies_for_Academic_and_Mental_Health": [
    "When juggling academics and mental health, coping strategies are key. One of the best ways to cope with academic pressure is by practicing deep breathing or grounding techniques when you feel overwhelmed. Taking short breaks and engaging in physical activity like stretching or walking can also help reduce stress. If you’re feeling mentally drained, use Serenimind’s Journals to reflect and our wellness goal setter to track stress-relieving activities. If the stress continues, booking a session with a therapist through Serenimind will provide you with professional support and personalized strategies.",
    
    "Effective coping starts with self-awareness. Recognize when you’re becoming overwhelmed and take immediate action to decompress. Deep breathing exercises, journaling, or engaging in your favorite hobby can provide an emotional reset. Serenimind’s Journals and wellness goal setter are perfect tools for managing this. If you’re struggling to cope with stress, a therapist can help guide you through additional strategies to ensure you’re handling both academic pressure and mental health.",
    
    "When dealing with academic stress, it’s essential to focus on controlling what you can. Start by developing a study routine that breaks tasks into smaller steps, helping reduce the feeling of being overwhelmed. Also, ensure that you’re giving yourself time to relax—taking a walk, reading, or engaging in a hobby can relieve stress. If you’re finding it difficult to manage your emotions, journaling in Serenimind can help, and booking a therapist can provide you with targeted support to help you cope more effectively.",
    
    "Coping with stress involves both mental and physical strategies. Start by acknowledging when you're stressed, then implement techniques like time management, exercise, or deep breathing to reset your focus. Regular check-ins with yourself can help you avoid burnout. If things feel unmanageable, try using Serenimind’s wellness goal setter to structure your day, and reach out to a therapist for extra support."
],


    "farewell": [
        "Take good care of yourself. Remember that you can always return when you need support.",
        "Goodbye for now. Be gentle with yourself, and know that support is always available here when you need it.",
        "Take care, and remember that every small step matters. I'm here whenever you need to talk.",
        "Wishing you well. Remember to be kind to yourself, and feel free to return anytime you need support.",
        "Goodbye. Remember that seeking support is a sign of strength, and you're welcome back anytime."
    ],
    'unknown': [
        "I'm not sure I fully understand. Could you rephrase that or provide more details?",
        "I'm still learning and growing. Can you tell me more about what you mean?",
        "I want to make sure I'm addressing your needs correctly. Could you elaborate on that?",
        "I'm not quite sure how to respond to that. Can you give me some more context?",
        "I'm afraid I don't have enough information to respond accurately. Could you clarify your question or statement?"
    ],  

            }

            # 7. Select random response for the predicted intent
            response_message = random.choice(responses.get(predicted_intent, responses["unknown"]))

            # 8. Store in database using the authenticated user
            conversation = UserConversation.objects.create(
                user=request.user,  # Use the authenticated user directly
                user_message=user_message,
                bot_response=response_message
            )

            # 9. Return response
            return Response({
                "response": response_message, 
                "intent": predicted_intent
            }, status=200)

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

    # Send notification email
    subject = 'New User Signup'
    message = f"A new user has signed up:\n\nFull Name: {first_name} {last_name}\nUsername: {username}\nEmail: {email}"
    recipient_list = ['team@serenimind.com.ng']

    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    except Exception as e:
        return Response({'errors': {'email': ['Failed to send email notification.']}}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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


@api_view(['GET'])
def blogpost_list(request):
    """Public list of blog posts ordered by newest first."""
    posts = BlogPost.objects.all().order_by('-created_at')
    serializer = BlogPostSerializer(posts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
def blogpost_detail(request, pk):
    """Retrieve a single blog post by id."""
    try:
        post = BlogPost.objects.get(pk=pk)
    except BlogPost.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = BlogPostSerializer(post, context={'request': request})
    return Response(serializer.data)
    
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

@permission_classes([IsAuthenticated])
class BotSettingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings, _ = BotSettings.objects.get_or_create(
            user=request.user,
            defaults={'bot_name': 'SereniAI'}
        )
        serializer = BotSettingsSerializer(settings)
        return Response(serializer.data)

    def put(self, request):
        settings, _ = BotSettings.objects.get_or_create(
            user=request.user,
            defaults={'bot_name': 'SereniAI'}
        )
        serializer = BotSettingsSerializer(settings, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Bot name updated successfully!", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Failed to update bot name.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
        
# AWS Rekognition Client
rekognition_client = boto3.client(
    'rekognition',
    aws_access_key_id='AKIAXTORPLPAIYQACTWZ',
    aws_secret_access_key='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',
    region_name='us-east-1'
)

@csrf_exempt
def detect_mood(request):
    if request.method == 'POST' and request.FILES.get('image'):
        # Save the uploaded image
        image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        file_path = fs.path(filename)

        try:
            # Read the image bytes
            with open(file_path, 'rb') as image_file:
                image_bytes = image_file.read()

            # Call Rekognition
            response = rekognition_client.detect_faces(
                Image={'Bytes': image_bytes},
                Attributes=['ALL']  # Include emotions in the response
            )

            # Parse emotions
            emotions = response['FaceDetails'][0]['Emotions']
            dominant_emotion = max(emotions, key=lambda e: e['Confidence'])
            mood = dominant_emotion['Type']

            # Clean up the file
            os.remove(file_path)

            return JsonResponse({
                'mood': mood,
                'message': f'You appear to be {mood.lower()}!',
                'details': emotions  # Optional: Send all emotions
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)

@api_view(["POST"])
def contact_view(request):
    data = request.data
    try:
        subject = "Timingotech - New Contact Form Submission"
        message = f"""
You have a new contact form submission:

Name: {data.get('name', '')}
Email: {data.get('email', '')}
Phone: {data.get('phone', '')}
Company: {data.get('company', '')}
Service Interest: {data.get('service_interest', '')}
Message: {data.get('message', '')}
"""
        send_mail(
            subject,
            message,
            "team@serenimind.com.ng",  # Must match EMAIL_HOST_USER in settings
            ["timingotech@gmail.com"],
            fail_silently=False,
        )
        return Response({"success": "Message sent successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ActivityMovieListView(generics.ListAPIView):
    """Read-only list of Activity Lounge movies. Public access."""
    queryset = ActivityMovie.objects.all().order_by('id')
    serializer_class = ActivityMovieSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        mood = self.request.query_params.get('mood')
        if mood:
            queryset = queryset.filter(moods__icontains=mood)
        return queryset


class ActivityGameListView(generics.ListAPIView):
    """Read-only list of Activity Lounge games. Public access."""
    queryset = ActivityGame.objects.all().order_by('id')
    serializer_class = ActivityGameSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        mood = self.request.query_params.get('mood')
        if mood:
            queryset = queryset.filter(moods__icontains=mood)
        return queryset


class ActivityExerciseListView(generics.ListAPIView):
    """Read-only list of Activity Lounge exercises. Public access."""
    queryset = ActivityExercise.objects.all().order_by('id')
    serializer_class = ActivityExerciseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        mood = self.request.query_params.get('mood')
        if mood:
            queryset = queryset.filter(moods__icontains(mood))
        return queryset


class ActivitySoundListView(generics.ListAPIView):
    """Read-only list of Activity Lounge sounds. Public access."""
    queryset = ActivitySound.objects.all().order_by('id')
    serializer_class = ActivitySoundSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        queryset = super().get_queryset()
        mood = self.request.query_params.get('mood')
        if mood:
            queryset = queryset.filter(moods__icontains=mood)
        return queryset