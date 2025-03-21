#users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.models import User
from .forms import SignUpForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from .forms import EmailUpdateForm
from django.contrib.auth import logout

def custom_logout_view(request):
    """Logs out the user and redirects to the home page or login page."""
    if request.method == "POST":  # Ensure logout happens only on POST request
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect("login")  # Redirect to login page or another page

    return redirect("home")  # Optional: handle GET requests gracefully


def is_superuser(user):
    """Check if the user is a superuser."""
    return user.is_superuser

@user_passes_test(is_superuser)
def user_list(request):
    """
    Display a list of all registered users.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered user list page.
    """
    users = User.objects.all()
    return render(request, 'users/user_list.html', {'users': users})


def profile(request, user_id):
    """
    Display the profile page of a specific user.

    Args:
        request (HttpRequest): The request object.
        user_id (int): The ID of the user whose profile is being viewed.

    Returns:
        HttpResponse: Rendered profile page of the specified user.
    """
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/profile.html', {'user': user})


def signup(request):
    """
    Handle user signup process.

    If the form is submitted and valid, a new user is created and logged in.
    Otherwise, an empty signup form is displayed.

    Args:
        request (HttpRequest): The request object.

    Returns:
        HttpResponse: Rendered signup page or redirect to the session list on success.
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password1"])  # ✅ Use 'password1'
            user.save()  # ✅ Don't forget to save the user!
            login(request, user)  # Log in after successful signup
            return redirect('home')
    else:
        form = SignUpForm()
    
    return render(request, 'registration/signup.html', {'form': form})

def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def edit_email(request, user_id):
    """Allow admin to update a user's email."""
    user = get_object_or_404(User, id=user_id)

    if request.method == "POST":
        form = EmailUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f"Email updated for {user.username}.")
            return redirect("users:user_list")
    else:
        form = EmailUpdateForm(instance=user)

    return render(request, "users/edit_email.html", {"form": form, "user": user})
    






