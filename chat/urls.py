# chat/urls.py
from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('lobby/', views.lobby, name="lobby"),
    path('select_room/', views.select_room, name='select_room'),  # Room selection page
    path('<str:room_name>/', views.room, name='room'),  # Chat room page
]
