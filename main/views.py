from django.shortcuts import render
from django.contrib.auth.models import User  
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views import View

@require_POST
def contact_view(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')

    # Here you would typically handle the form data (e.g., send an email, save to a database, etc.)
    # For now, we'll just return a simple response.
    return HttpResponse(f'Thank you for your message, {name}!')

@login_required
def home(request):
    return render(request, 'main/home.html', {'user': request.user})


def about(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'main/about.html', {'users': users}) 

def contacts(request):
    users = User.objects.all()  # Fetch all users
    return render(request, 'main/contacts.html', {'users': users})  # Pass users to the template


