from django.urls import path
from . import views
from .views import create_voting_session
from django.contrib.auth import views as auth_views
from .views import register  # Import the registration view
from django.contrib.auth.views import LogoutView
from . import utils
from .views import stop_voting_session, create_voting_session

urlpatterns = [
    path('', views.index, name='index'),
    path('vote_view/<int:session_id>/', views.vote_view, name='vote_view'),
    path('results/<int:session_id>/', views.results_view, name='results'),
    path('create-session/', create_voting_session, name='create_voting_session'),
    path('results/', views.general_results_view, name='general_results'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register, name='registration'),  # Add this line for registration
    path('send-voting-invitation/', utils.send_voting_invitation, name='send_voting_invitation'),
    path('start-voting/<int:session_id>/', views.start_voting_session, name='start_voting_session'),
    path('stop-voting/<int:session_id>/', stop_voting_session, name='stop_voting_session'),
    path('create-session/', create_voting_session, name='create_voting_session'),

]

