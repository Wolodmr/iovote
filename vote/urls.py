from django.urls import path
from . import views

urlpatterns = [
    path('<int:session_id>/', views.vote, name='vote'),
    path('<int:session_id>', views.vote, name='vote'),  # Without the trailing slash
    path('thank-you/', views.thank_you, name='thank_you'),
]
