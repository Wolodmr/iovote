# voting_sessions/urls.py
from django.urls import path
from . import views  # Import views from the current module
from .views import session_invite, vote


app_name = "voting_sessions"

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path('<int:session_id>/', views.session_detail, name='session_detail'),
    path("vote/<int:session_id>/", vote, name="vote"),  # Ensure this line exists!
    path('invite/<uuid:session_uuid>/', session_invite, name='session_invite'),
]


