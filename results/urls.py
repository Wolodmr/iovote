# results/urls.py
from django.urls import path
from . import views

app_name = 'results'

urlpatterns = [
    path('<int:session_id>/', views.results_list, name='results_list'),
    path('<int:session_id>/detail/', views.results_detail, name='results_detail'),
     path('<int:session_id>/results/', views.results_detail, name='results_detail'),
]

