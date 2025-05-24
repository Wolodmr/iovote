# results/urls.py
from django.urls import path
from . import views
from .views import results_dashboard
# from django_plotly_dash.views import add_to_session
from django.views.generic import TemplateView
from django.urls import path, include




app_name = 'results'

urlpatterns = [
    path('', views.results_list, name='results_list'),
    path("dashboard/", results_dashboard, name="results_dashboard"),  
    path('<int:session_id>/detail/', views.results_detail, name='results_detail'),
    path('<int:session_id>/results/', views.results_detail, name='results_detail'),  # Duplicate URL pattern
    path('dashboard/', TemplateView.as_view(template_name='results/dashboard.html'), name='dashboard'),
    path('dashboard/', views.results_dashboard, name='results_dashboard'),  # Django view
    
    
]


