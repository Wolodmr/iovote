from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('room/', views.single_room, name='single_room'),
]
