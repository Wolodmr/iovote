from django.urls import path
from . import views

urlpatterns = [
    path('room/', views.single_room, name='single_room'),
]
