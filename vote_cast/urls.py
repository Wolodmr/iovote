from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Main app URLs
    path('users/', include('users.urls', namespace='users')),  # Users app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # This includes the login, logout, password change, etc.
    path("voting_sessions/", include("voting_sessions.urls", namespace="voting_sessions")),  # Include the voting_sessions URLs
    path('results/', include('results.urls')),  # Include the results app URLs
    path('vote/', include('vote.urls')),  # Corrected path inclusion for the vote app
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.BASE_DIR)

