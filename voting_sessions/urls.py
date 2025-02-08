# sessions/urls.py
from django.urls import path
from . import views

app_name = "voting_sessions"

urlpatterns = [
    path("", views.session_list, name="session_list"),  # List all sessions
    path("<int:session_id>/", views.session_detail, name="session_detail"),  # View session details
    
]

