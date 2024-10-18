from django.urls import path
from . import views
from .views import create_voting_session
from django.contrib.auth import views as auth_views
from .views import register  # Import the registration view
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:session_id>/', views.vote, name='vote'),
    path('results/<int:session_id>/', views.results_view, name='results'),
    path('create-session/', create_voting_session, name='create_voting_session'),
    path('results/', views.general_results_view, name='general_results'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='registration'),  # Add this line for registration
    path('send-test-email/', views.send_test_email, name='send_test_email'),
]

