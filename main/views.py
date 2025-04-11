from django.shortcuts import render, redirect
from django.contrib.auth.models import User  
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.views.decorators.http import require_POST

@require_POST
def contact_view(request):
    """Handles contact form submission and sends email to the admin."""
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')

    if not (name and email and message):
        messages.error(request, "All fields are required.")
        return redirect("contacts")

    # ✅ Compose email content
    subject = f"New Contact Form Submission from {name}"
    email_message = f"Sender Name: {name}\nSender Email: {email}\n\nMessage:\n{message}"

    # ✅ Get admin email from settings
    admin_email = settings.DEFAULT_FROM_EMAIL

    try:
        send_mail(
            subject, 
            email_message, 
            email,  # Reply-to sender's email
            [admin_email],  # Send to admin
            fail_silently=False
        )
        messages.success(request, "Your message has been sent successfully!")
    except Exception as e:
        messages.error(request, f"Error sending email: {e}")

    return redirect("contacts")

def home(request):
    """Renders the home page."""
    return render(request, 'main/home.html')

def about(request):
    """Renders the about page with a list of all users."""
    users = User.objects.only("id", "username")  # ✅ Optimize by selecting only needed fields
    return render(request, 'main/about.html', {'users': users})

def contacts(request):
    """Renders the contacts page."""
    return render(request, 'main/contacts.html')
