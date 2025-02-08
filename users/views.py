from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

def user_list(request):    
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile.html', {'user': user})


