#main/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User  
from django.http import HttpResponse
from django.views.decorators.http import require_POST

@require_POST
def contact_view(request):
    """Handles contact form submission."""
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')

    # You can add logic here (e.g., send an email, save to DB, etc.)
    return HttpResponse(f'Thank you for your message, {name}!')

def home(request):
    """Renders the home page."""
    return render(request, 'main/home.html')

def about(request):
    """Renders the about page with a list of all users."""
    users = User.objects.all()
    return render(request, 'main/about.html', {'users': users})

def contacts(request):
    """Renders the contacts page with a list of all users."""
    users = User.objects.all()
    return render(request, 'main/contacts.html', {'users': users})


