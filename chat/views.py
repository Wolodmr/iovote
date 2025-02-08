from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.timezone import now

@login_required
def single_room(request):
    return render(request, 'chat/room.html', {'timestamp': now().timestamp()})

