from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'autocapitalize': 'none',
            'autocorrect': 'off',
            'autocomplete': 'username',
        })
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username__iexact=username).exists():
            raise forms.ValidationError("This username is already in use.")
        return username

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
