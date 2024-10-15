from django import forms
from .models import VotingOption, VotingSession

class VotingForm(forms.Form):
    options = forms.ModelMultipleChoiceField(
        queryset=VotingOption.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    no_support = forms.BooleanField(required=False, label="I don't support any of the proposed options")

class VotingSessionForm(forms.ModelForm):
    class Meta:
        model = VotingSession
        fields = ['name', 'start_date', 'end_date']  # Add fields relevant to a voting session

