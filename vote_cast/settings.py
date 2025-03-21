"""
Django settings for vote_cast project.
"""

from pathlib import Path
import os
import logging
from decouple import config
import sys

# Define the project base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
SECRET_KEY = config('DJANGO_SECRET_KEY', default='default-secret-key')
DEBUG = config('DJANGO_DEBUG', default=True, cast=bool)

# Ensure ALLOWED_HOSTS is always a list
ALLOWED_HOSTS = config('DJANGO_ALLOWED_HOSTS', default="127.0.0.1,localhost").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    "debug_toolbar",
    'django_plotly_dash',
    'results',
    "channels",
    'crispy_forms',

    'main',
    'users',   
    'voting_sessions',
    'vote',
    
]

MIDDLEWARE = [
    "csp.middleware.CSPMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "django_plotly_dash.middleware.BaseMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

CSP_FRAME_ANCESTORS = ["'self'"]  # Allows only the same origin to embed iframes
CSP_DEFAULT_SRC = ["'self'"]  
CSP_SCRIPT_SRC = ["'self'", "'unsafe-inline'", "https://cdn.plot.ly"]
CSP_STYLE_SRC = ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"]


X_FRAME_OPTIONS = "SAMEORIGIN"  # Allow iframes on the same domain

PLOTLY_DASH = {
    "ws_route": "",  # Disable WebSockets
    "http_plotly_component_prefix": "dash/",
    "serve_locally": True,  # Serve JavaScript and CSS locally
    "expose_javascript": True,  # Allow Plotly.js to be exposed
}


INTERNAL_IPS = ["127.0.0.1"]

SITE_URL = "http://127.0.0.1:8000"  # Change this to your production domain

ROOT_URLCONF = 'vote_cast.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'main/templates/main',
            BASE_DIR / 'users/templates/users',
            BASE_DIR / 'vote/templates/vote',
            BASE_DIR / 'results/templates/results',
            BASE_DIR / 'voting_sessions/templates/voting_sessions',
        ],     
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

from django.urls import reverse_lazy

LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = '/voting_sessions/'

WSGI_APPLICATION = 'vote_cast.wsgi.application'
ASGI_APPLICATION = 'vote_cast.asgi.application'

# Database Configuration (SQLite for now)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

CSRF_COOKIE_HTTPONLY = False  # ✅ Must be False (Default)
CSRF_COOKIE_SECURE = False  # ✅ Set to False for local developmen

# Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Berlin'  # Change "CET" to a proper Django-compatible timezone
USE_I18N = True
USE_TZ = True

# Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
    BASE_DIR / 'main/static',
    BASE_DIR / 'users/static',
]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
]

# Email Configuration (Loaded from .env)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_FAIL_SILENTLY = False

# Test Email Backend
if "test" in sys.argv:
    DEBUG = True
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    EMAIL_HOST = ""
    EMAIL_PORT = ""
    logging.getLogger(__name__).debug(f"✅ Using {EMAIL_BACKEND} for tests")

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}
