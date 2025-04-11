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
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        """Ensure email is unique in a more optimized way."""
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():  # ✅ More efficient than `count()`
            raise forms.ValidationError("This email is already in use.")
        return email


class EmailUpdateForm(forms.ModelForm):
    """Form for updating a user's email while ensuring uniqueness."""

    class Meta:
        model = User
        fields = ["email"]

    def clean_email(self):
        """Ensure the email is unique excluding the current user."""
        email = self.cleaned_data.get("email")
        user_id = self.instance.pk  # Get the current user's ID

        if User.objects.exclude(pk=user_id).filter(email=email).exists():  # ✅ Avoids redundant queries
            raise forms.ValidationError("This email is already in use.")
        return email
