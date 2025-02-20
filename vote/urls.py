from django.urls import path
from . import views

app_name = 'vote'

urlpatterns = [
    path('<int:session_id>/', views.vote, name='vote'),
    path('<int:session_id>/<int:option_id>/submit/', views.results_detail, name='results_detail'),
]

