"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 5.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
from django.conf import global_settings
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-bot(2wug8-7lj_o5oo0!e#!i@xtzx8ypj=t(5uj^d=br4uxt^b'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True        

ALLOWED_HOSTS = ['.vercel.app','now.sh','timithemagician.pythonanywhere.com','localhost','.render.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'api',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_rest_passwordreset',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist'

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
     'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
      ],
}

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'backend.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

DATABASES ["default"] = dj_database_url.parse("postgres://testdb_zsxo_user:4Uk7Nc5I6NcFmYFlLlYcm1RKACx5tYy9@dpg-co1j8pn79t8c73celqfg-a.oregon-postgres.render.com/testdb_zsxo")




# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465  # or 465 for SSL
EMAIL_USE_TLS = False  # or False for SSL
EMAIL_USE_SSL = True  # or True for SSL
EMAIL_HOST_USER = 'timingotech@gmail.com'  
EMAIL_HOST_PASSWORD = 'pzkgiumwdbexrcgb'    

CORS_ORIGIN_ALLOW_ALL = True    

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://serenimindbackend.onrender.com" 
]
CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    'http://serenimindbackend.onrender.com',
)
CORS_ALLOW_METHODS = [
    'GET',
    'POST',
]

CORS_ALLOW_HEADERS = [
    'Content-Type',
    'Authorization',
    # Add other allowed headers as needed
]
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://serenimindbackend.onrender.com'
    ]
CSRF_COOKIE_SECURE = True  # For secure connections (HTTPS)
CSRF_COOKIE_HTTPONLY = True  # Restrict cookie access to JavaScript
CSRF_COOKIE_SAMESITE = 'Lax'  # Adjust as needed (Lax, Strict, None)
CSRF_COOKIE_NAME = 'X_CSRFTOKEN'
CSRF_HEADER_NAME = 'HTTP_X_CSRFTOKEN'



CSRF_COOKIE_NAME = getattr(global_settings, 'CSRF_COOKIE_NAME', 'X_CSRFTOKEN')

CACHES = {
    'default': {    
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',  # Provide a unique identifier for the cache
    }
}

SIMPLE_JWT = {
     'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
     'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
     'ROTATE_REFRESH_TOKENS': True,
     'BLACKLIST_AFTER_ROTATION': True
}
