from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import signup, login ,csrf_token, submit_form,logout_view, get_user_data, send_verification_email, verification,  password_reset,MessageListCreateAPIView,  MessageListCreate, MessageRetrieveUpdateDestroy, MessageDetailView, MessageEditView, MessageDeleteView,get_user_info_dashboard, delete_account
from . import views 
from rest_framework import routers
from .views import CommunityViewSet, MyTokenObtainPairView, get_user_data, SenderIdAPIView, get_user_username, UserSettingsView, MoodEntryListCreateAPIView, MoodEntryRetrieveUpdateDestroyAPIView, CommunityViewSet, DeleteUserAccountView, send_email, subscribe_newsletter, MoodAssessmentView, ChatbotView
from rest_framework_simplejwt.views import (
    
    TokenRefreshView,
)
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter
from .views import TodoViewSet, MoodEntryViewSet
from .views import BotSettingsView, detect_mood
from .views import contact_view
from .views import ActivityMovieListView, ActivityGameListView, ActivityExerciseListView, ActivitySoundListView
from .views_chat_enhanced import (
    EnhancedChatView,
    ConversationHistoryView,
    ConversationAnalyticsView,
    DeleteConversationView,
    ConversationLogView,
    ChatThreadListCreateView,
    ChatThreadDetailView,
    ChatThreadMessagesView
)

router = DefaultRouter()
router.register(r'todos', TodoViewSet)
router.register(r'mood-entries', MoodEntryViewSet)

router = routers.DefaultRouter()
router.register(r'communities', CommunityViewSet)
     
urlpatterns = [
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('signup/', signup, name='signup'),
    path('verification/', verification, name='verification'),
    path('send-verification-email/', send_verification_email, name='send_verification_email'),
    path('csrf/', csrf_token, name='csrf_token'),
    path('submit-form/', submit_form, name='submit_form'),
    path('profiles/<str:username>/', views.get_user_profile),
    path('profiles/<str:sername>/update/', views.update_user_profile),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('logout/', views.LogoutView.as_view(), name ='logout'), 
    path('user/', get_user_data, name='user_data'),
    path('create-blog/', views.create_blog, name='create_blog'),
    path('blog-posts/', views.blogpost_list, name='blogpost_list'),
    path('blog-posts/<int:pk>/', views.blogpost_detail, name='blogpost_detail'),
    path('journal-entries/', views.journal_entries),
    path('journal-entries/<int:pk>/', views.journal_entry_detail),
    path('community/<int:community_id>/messages/', MessageListCreate.as_view(), name='message-list-create'),
    path('community/<int:community_id>/messages/', MessageListCreateAPIView.as_view()),
    path('', include(router.urls)),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('message/<int:pk>/edit/', MessageEditView.as_view(), name='message-edit'),
    path('message/<int:pk>/delete/', MessageDeleteView.as_view(), name='message-delete'),
    path('user-info-dashboard/', get_user_info_dashboard, name='user-info-dashboard'),
    path('get-user-username/', get_user_username, name='get-user-username'),
    path('login/', views.login, name='login'),
    path('token/', jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'),
    path('messages/<int:message_id>/sender/', SenderIdAPIView.as_view(), name='sender_id_api'),
    path('settings/', UserSettingsView.as_view(), name='user-settings'),
    path('open-library-proxy/', views.open_library_proxy, name='open_library_proxy'),
    path('todos/', views.todos_list_create, name='todos-list-create'),
    path('todos/<int:pk>/', views.todo_detail_update_delete, name='todo-detail-update-delete'),
    path('todos/<int:todo_id>/complete/', views.complete_todo, name='complete_todo'),
    path('mood-entries/', MoodEntryListCreateAPIView.as_view(), name='mood-entry-list-create'),
    path('mood-entries/<int:pk>/', MoodEntryRetrieveUpdateDestroyAPIView.as_view(), name='mood-entry-detail'),
    path('users/<int:user_id>/', DeleteUserAccountView.as_view(), name='delete_user_account'),
    path('delete-account/', delete_account, name='delete_account'),
    path('send-email/', send_email, name='send_email'),
    path('subscribe-newsletter/', subscribe_newsletter, name='subscribe_newsletter'),
    path('mood-assessment/', MoodAssessmentView.as_view(), name='mood_assessment'),
    path('report-message/<int:message_id>/', views.report_message, name='report_message'),
    path('chat/', ChatbotView.as_view(), name='chat'),
    
    # Enhanced chat endpoints with history and context
    path('chat/enhanced/', EnhancedChatView.as_view(), name='chat-enhanced'),
    path('chat/history/', ConversationHistoryView.as_view(), name='chat-history'),
    path('chat/analytics/', ConversationAnalyticsView.as_view(), name='chat-analytics'),
    path('chat/history/delete/', DeleteConversationView.as_view(), name='chat-delete-all'),
    path('chat/history/<int:conversation_id>/delete/', DeleteConversationView.as_view(), name='chat-delete-one'),
    path('chat/history/log/', ConversationLogView.as_view(), name='chat-log'),
    path('chat/threads/', ChatThreadListCreateView.as_view(), name='chat-thread-list'),
    path('chat/threads/<int:thread_id>/', ChatThreadDetailView.as_view(), name='chat-thread-detail'),
    path('chat/threads/<int:thread_id>/messages/', ChatThreadMessagesView.as_view(), name='chat-thread-messages'),
    
    path('bot-settings/', BotSettingsView.as_view(), name='bot-settings'),
    path('detect-mood/', detect_mood, name='detect_mood'),
    path("contact/", contact_view, name="contact"),

    # Activity Lounge content (read-only, public)
    path('activity/movies/', ActivityMovieListView.as_view(), name='activity-movies'),
    path('activity/games/', ActivityGameListView.as_view(), name='activity-games'),
    path('activity/exercises/', ActivityExerciseListView.as_view(), name='activity-exercises'),
    path('activity/sounds/', ActivitySoundListView.as_view(), name='activity-sounds'),

]


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthenticastion',
#     )
# }
 