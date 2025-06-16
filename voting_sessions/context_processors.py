from django.utils import timezone
from .models import Session
from .models import SessionAccess

def latest_session(request):
    if request.user.is_authenticated:
        access = SessionAccess.objects.filter(user=request.user).order_by('-accessed_at').first()
        return {'latest_session_id': access.session.id if access else None}
    return {'latest_session_id': None}

