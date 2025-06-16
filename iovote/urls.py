#iovote/urls.py
from django.views.generic import RedirectView
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import debug_toolbar

urlpatterns = [
    
    path('favicon.ico', RedirectView.as_view(url='/static/images/favicon.ico', permanent=True)),
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Main app URLs
    path('users/', include('users.urls', namespace='users')),  # Users app URLs
    path('', include('django.contrib.auth.urls')),  # This includes the login, logout, password change, etc.
    path("voting_sessions/", include("voting_sessions.urls", namespace="voting_sessions")),  # Include the voting_sessions URLs
    path('results/', include('results.urls')),  # Include the results app URLs
    path('vote/', include('vote.urls')),  # Corrected path inclusion for the vote app
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.BASE_DIR)
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
    
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError

try:
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "adminpassword123")
        print("✅ Superuser 'admin' created")
except IntegrityError:
    pass
except Exception as e:
    print(f"⚠️ Error creating superuser: {e}")




