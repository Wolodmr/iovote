from vote_cast.settings import *

# # Override email settings for testing
# EMAIL_HOST_USER = "postvezha@gmail.com"
# EMAIL_HOST_PASSWORD = 'auflnoyhnkyigmfr'

# # Use an in-memory database for faster testing
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": ":memory:",
#     }
# }
os.environ["EMAIL_BACKEND"] = "django.core.mail.backends.locmem.EmailBackend"
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND")

