# chat/views.py
from django.shortcuts import render, redirect

def lobby(request):
    return render(request, "chat/lobby.html")

def select_room(request):
    room_name = request.GET.get('room_name')
    if room_name:
        return redirect('chat:room', room_name=room_name)
    return render(request, 'chat/select_room.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {'room_name': room_name})
