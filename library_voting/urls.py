from django.contrib import admin
from django.urls import path, include
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # Main app URLs
    path('users/', include('users.urls', namespace='users')),  # Users app URLs
    path('accounts/', include('django.contrib.auth.urls')),  # This includes the login, logout, password change, etc.
    path('chat/', include('chat.urls')),  # Include the chat URLs
    # path('voting_sessions/', include('voting_sessions.urls')),  # Voting sessions app URLs
    # path('preliminary_voting/', include('preliminary_voting.urls')),  # Preliminary voting app URLs
    # path('main_voting/', include('main_voting.urls')),  # Main voting app URLs
]
