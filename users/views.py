#users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from .forms import SignUpForm
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User

class CustomLogoutView(View):
    def post(self, request):
        logout(request)
        # return redirect('home')
    
def user_list(request):    
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})

def profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile.html', {'user': user})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after successful registration
            return redirect('voting_sessions:session_list')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})



