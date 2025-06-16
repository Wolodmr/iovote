from .settings import *
from django.test import TestCase
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class MyTestCase(TestCase):
    def setUp(self):
        # Log current EMAIL_BACKEND setting to debug
        logger.debug(f"EMAIL_BACKEND: {settings.EMAIL_BACKEND}")
        
        # Override the EMAIL_BACKEND for the test to use locmem backend
        settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
        

print('ONE')
from django.core.mail import get_connection

# Force test email backend
get_connection(backend="django.core.mail.backends.locmem.EmailBackend")


# Force test email backend
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Explicitly remove SMTP settings

EMAIL_PORT = ""
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_HOST_USER = "postvezha@gmail.com"
EMAIL_HOST_PASSWORD = "ljosehygsmlcunls"

# Debug print to confirm override
print(f"✅ Loaded EMAIL_BACKEND: {EMAIL_BACKEND}")
