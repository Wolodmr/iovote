# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    """
    A form for user registration extending Django's built-in UserCreationForm.
    
    Fields:
        - username: The unique username of the user.
        - email: A required email field.
        - password1: The user's password.
        - password2: Confirmation for the password.
    """
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        
    def clean_email(self):
            """Ensure email is unique."""
            email = self.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                raise forms.ValidationError("This email is already in use.")
            return email
class EmailUpdateForm(forms.ModelForm):
    """Form for admin to update a user's email."""
    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        """Ensure email is unique."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email
