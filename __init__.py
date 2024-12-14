from __future__ import absolute_import, unicode_literals

# This ensures that the Celery app is always imported
# when Django starts.
from .celery_app import app as celery_app

__all__ = ('celery_app',)
