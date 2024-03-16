from django.urls import path, include
from django.contrib.auth import views as auth_views
from .views import signup, login_view ,csrf_token, submit_form,logout_view, get_user_data, send_verification_email, verification,  password_reset
from . import views

urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login_view, name='login'),
     path('resetpassword/', password_reset, name='password_reset'),
     path('verification/', verification, name='verification'),
     path('send-verification-email/', send_verification_email, name='send_verification_email'),
    path('csrf/', csrf_token, name='csrf_token'),
    path('submit-form/', submit_form, name='submit_form'),
    path('profiles/<str:username>/', views.get_user_profile),
    path('profiles/<str:username>/update/', views.update_user_profile),
    path('posts/', views.post_list, name='post_list'),
    path('posts/create/', views.post_create, name='post_create'),
    path('logout/', logout_view, name='logout'),
    path('user/', get_user_data, name='user_data'),
    path('send-verification-email/', send_verification_email, name='send_verification_email'),


]


# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     )
# }
