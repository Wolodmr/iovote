"""
Django settings for vote_cast project.
"""

import os
import sys
import logging
from pathlib import Path
from decouple import config

# 📌 Project Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

CSRF_TRUSTED_ORIGINS = ['https://votecast-production.up.railway.app']


# 📌 Security & Debugging
SECRET_KEY = config('DJANGO_SECRET_KEY', default='default-secret-key')
DEBUG = True
ALLOWED_HOSTS = ['votecast-production.up.railway.app', '127.0.0.1', 'localhost']
DEFAULT_FROM_EMAIL = 'postvezha@gmail.com'

# ✅ Installed Applications
INSTALLED_APPS = [
    # Django Default Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'rest_framework',
    'django_plotly_dash',
    'crispy_forms',

    # Local Apps
    'main',
    'users',
    'voting_sessions',
    'vote',
    'results',
]

# ✅ Middleware Configuration
MIDDLEWARE = [
    # Security & Performance
    "csp.middleware.CSPMiddleware",
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",

    # Cache Middleware
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

    # Django Default Middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    # Django Plotly Dash Middleware
    "django_plotly_dash.middleware.BaseMiddleware",
]

if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")


# ✅ Django Debug Toolbar
INTERNAL_IPS = ["127.0.0.1"]

# ✅ Caching Configuration
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': BASE_DIR / 'cache',
        'TIMEOUT': 600,  # 10 minutes
        'OPTIONS': {'MAX_ENTRIES': 1000}
    }
}

# ✅ Content Security Policy (CSP)
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net", "https://cdnjs.cloudflare.com")
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'", "https://cdn.plot.ly", "https://code.jquery.com", "https://cdn.jsdelivr.net", "https://stackpath.bootstrapcdn.com")
CSP_FONT_SRC = ("'self'", "https://fonts.gstatic.com", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net")
CSP_IMG_SRC = ("'self'", "data:")

# ✅ Allow Embedding Dash Apps in Iframes
X_FRAME_OPTIONS = "SAMEORIGIN"

# ✅ Plotly Dash Configuration
PLOTLY_DASH = {
    "ws_route": "",  # Disable WebSockets
    "http_plotly_component_prefix": "dash/",
    "serve_locally": True,
    "expose_javascript": True,
}

# ✅ URL Configuration
SITE_URL = "http://127.0.0.1:8000"
ROOT_URLCONF = 'vote_cast.urls'

# ✅ Template Settings
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

# ✅ Authentication
from django.urls import reverse_lazy
LOGIN_URL = reverse_lazy('login')
LOGIN_REDIRECT_URL = '/voting_sessions/'

# ✅ WSGI & ASGI Applications
WSGI_APPLICATION = 'vote_cast.wsgi.application'
ASGI_APPLICATION = 'vote_cast.asgi.application'

# ✅ Database Configuration (SQLite)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ✅ Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ✅ CSRF Configuration
CSRF_COOKIE_HTTPONLY = False
CSRF_COOKIE_SECURE = False  # Set to False for local development

# ✅ Localization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'CET'  # Adjust timezone as needed
USE_I18N = True
USE_TZ = True

# ✅ Static Files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"    # used by collectstatic
STATICFILES_DIRS = [BASE_DIR / "static"] 
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django_plotly_dash.finders.DashAssetFinder',
    'django_plotly_dash.finders.DashComponentFinder',
]

# ✅ Email Configuration
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_FAIL_SILENTLY = False

# 📌 Use in Tests
if "test" in sys.argv:
    DEBUG = True
    EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    EMAIL_HOST = ""
    EMAIL_PORT = ""
    logging.getLogger(__name__).debug(f"✅ Using {EMAIL_BACKEND} for tests")

# ✅ Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['file'],
        },
        'voting_sessions.management.commands.send_notifications': {
            'level': 'INFO',
            'handlers': ['file'],
            'propagate': False,
        },
    },
}
