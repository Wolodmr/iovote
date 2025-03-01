from .settings import *  # Import all base settings

# Override email settings for testing
EMAIL_HOST_USER = "postvezha@gmail.com"
EMAIL_HOST_PASSWORD = 'auflnoyhnkyigmfr'

# Use an in-memory database for faster testing
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
