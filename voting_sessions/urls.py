# voting_sessions/urls.py
from django.urls import path
from . import views
from .views import session_invite, vote

app_name = "voting_sessions"

urlpatterns = [
    path('', views.session_list, name='session_list'),
    path("vote/<int:session_id>/", vote, name="vote"), 
    path('invite/<uuid:session_uuid>/', session_invite, name='session_invite'),
    # path('results/<int:session_id>/', views.results, name='session_results'),
    path('session/<int:session_id>/', views.session_detail, name='session_detail'),
    # path('session/<int:session_id>/charts/', views.session_charts, name='session_charts'),
    path('charts/', views.charts_redirect_view, name='charts'),
    path('charts/<int:session_id>/', views.session_charts, name='session_charts'),
    path('voting_sessions/session/<int:session_id>/charts/', views.session_charts, name='session_charts'),
]
