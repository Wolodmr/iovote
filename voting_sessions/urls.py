# voting_sessions/urls.py
from django.urls import path
from . import views  # Import views from the current module

app_name = "voting_sessions"

urlpatterns = [
   path('', views.session_list, name='session_list'),
    path('<int:session_id>/', views.session_detail, name='session_detail'),
    path('<int:session_id>/vote/', views.vote, name='vote'),  # Ensure this matches your view name
]


