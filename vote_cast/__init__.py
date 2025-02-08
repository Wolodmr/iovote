from __future__ import absolute_import, unicode_literals

# This ensures the Celery app is loaded when Django starts
from vote_cast.celery_app import app as celery_app


__all__ = ('celery_app',)
